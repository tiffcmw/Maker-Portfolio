from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View
from django.utils import timezone
from django.db import transaction

from .models import Message
from rest_framework.parsers import JSONParser
import cohere
import traceback

# Initialize Cohere client with API key
co = cohere.Client('my-cohere-api-key') # privacy reasons, replaced it

@method_decorator(csrf_exempt, name='dispatch')
class ChatView(View):
    # handler for GET requests
    # when the frontend makes a GET request to the backend, it will call this function
    def get(self, request, *args, **kwargs):
        # from models.py, Message is a class, and a table in the database. 
        # this line queries the database for all Message objects, and then order them chronologically according to the timestap
        # it is important for showing the past messages in the order order. 
        # these exact fields are present in the Message class in models.py,
        # and values allow to fetch only these fields. 
        # these fields are needed for the frontend to display the messages

        # for now its just fetching ALL past message from the message table in the database, 
        # becase i have not implemented an authentication system to the chat
        messages = list(Message.objects.order_by('timestamp').values(
            'message_id', 'sender__username', 'recipient__username', 'message_text', 'timestamp'
        ))
        # the JsonReppnse function returns the messages above in json format, 
        # with the key 'messages' and the value being the list of messages
        return JsonResponse({'messages': messages})

    def post(self, request, *args, **kwargs):
        # because i'm using django's default user model to store user details, 
        # i imported get_user_model() to enable easy access to the user model
        User = get_user_model()
        
        try:
            # Parse the incoming message from the frontend, store it in data variable
            data = JSONParser().parse(request)
            # get the message from the data variable like a key. 
            # this is text which the user inputted in the frontend text box, 
            # from line 186 in frontend/src/chat.js, the message state variable is posted in a json format. 
            user_message_text = data.get('message')
            
            # this checks if user_message_text is empty, and if it is, it raises an error
            if not user_message_text:
                raise ValidationError("No message provided.")
            
            # Fetch the last 5 exchanges from the database
            # why? I am using cohere's chat api https://docs.cohere.com/reference/chat
            # which has parameters for chat_history. which is good, because it allows the response to 
            # be more contextual and adapted to the user's previous messages.
            # i fetched the first 6 messages by reversed time, which means descening order of time. 
            # this way, the most recent 6 messages are used. 
            last_messages = Message.objects.order_by('-timestamp')[:5]
            
            # Create a list of dictionaries with last_messages. 
            # the requirements for chat history is aas such:
            # chat_history=[
            #   {"role": "USER", "message": "Who discovered gravity?"},
            #   {"role": "CHATBOT", "message": "The man who is widely credited with discovering gravity is Sir Isaac Newton"}
            # ]
            
            # Initialize an empty list for the chat history
            chat_history = []

            # Loop over the last messages in reverse order
            for message in reversed(last_messages):
                # messages in last_messages are from the message table in the database which has the sender column
                # message.sender.username points to the username
                # if the username is 'user', then the role is 'USER', else it is 'CHATBOT'
                # currently i'm only developing locally and user is my username, so the message i sent will def be USER
                # for widespread application, user if username !== 'ai' else chatbot should work, 
                # because message by ai is created in the database under username ai, always, under line 172
                role = 'USER' if message.sender.username == 'user' else 'CHATBOT'
                
                # Create a dictionary for the message
                # the role is from the previous line, 
                # message.message_text points to the actual message. also a column in the message table.
                # does not need to be index for alignment or anything, because both items are accesing the same message from last_messages.
                message_dict = {
                    'role': role,
                    'message': message.message_text
                }
                
                # Add the dictionary to the chat history
                chat_history.append(message_dict)
            
            # fun part where the magic kind of happens
            # this is the api request for the cohere chat api. 
            # the response is saved as the variable response. 
            # chat_history is the dictionary of the last 6 messages,
            # message is the user's message from the frontend.
            # prompt_truncation is a parameter that i set as attempt to decrease the length of the response, 
            # but it doesn't really work.
            # temperature tunes the degree of randomness in generation. lower values means more predictable, higher values means more random.
            # k means that the top k most likely tokens are considered for generation.
            # 10 tokens are very low, which means it selects only the 10 words with the highest probability of being the next word in text generation. 
            # less samples make less randomness in generation, which is what i want in this case for a conversational and conventional chat function,
            # which i want to stimulate reality. 
            response = co.chat(
                model="command-light",
                chat_history=chat_history,
                message=user_message_text,
                prompt_truncation="AUTO",
                temperature=0.2,
                k=10
            )
            
            # this is a sample reponse from the cohere chat api.
            """ cohere.Chat {
                id: 97bb6e40-8265-4b54-a045-8df18cccecc0
                response_id: 97bb6e40-8265-4b54-a045-8df18cccecc0
                generation_id: 224502bb-f920-49d4-98c5-6e4ebd073e6d
                message: ok
                text: the-actual-response, it's too long 
                conversation_id: None
                prompt: None
                chat_history: None
                preamble: None
                client: <cohere.client.Client object at 0x105e98620>
                token_count: {'prompt_tokens': 479, 'response_tokens': 296, 'total_tokens': 775, 'billed_tokens': 750}
                meta: {'api_version': {'version': '1'}, 'billed_units': {'input_tokens': 454, 'output_tokens': 296}}
                is_search_required: None
                citations: None
                documents: None
                search_results: None
                search_queries: None
            } """
            
            # the ai's reponse has the key 'text',
            # so response.text points to the actual response. save it to ai_message_text.
            ai_message_text = response.text

            # transaction.atmoic() is a context manager that wraps a block of code into a database transaction.
            # it just seemed like a very suave and clean way to handle the database interaction. 
            # this block executes immedialtey after the previous code.     
            with transaction.atomic():
                # Get or create the User instances for the user and the AI
                # i added this when i got errors trying to run the chat as a local user (with name 'user'), 
                # because I am not registerd in the user database. 
                # so i created this to create me as a user. 
                
                # the get_or_create method combines http request functionalities of get and create. 
                # it tries to get the user named user, if that fails it creates a user named user, same thing for ai. 
                # it helped create the user at start but then now that they are registered in the database, 
                # just get will work okay to fetch the user and ai object from the Uer table. 
                user, _ = User.objects.get_or_create(username='user')
                ai, _ = User.objects.get_or_create(username='ai')

                # testing locally will always result in sender being user, so i put sender as user.
                # later when I consider large scale user implementations, user will be replaced by the actual username. 

                # Create the user's message
                user_message = Message.objects.create(
                    sender=user,
                    recipient=ai,
                    is_from_ai=False, 
                    # user message fetched in line 47 
                    message_text=user_message_text,
                    language='en', 
                    timestamp=timezone.now()
                )

                # Create the AI's response message
                ai_message = Message.objects.create(
                    sender=ai,
                    recipient=user,
                    is_from_ai=True,
                    # ai api response from line 137
                    message_text=ai_message_text,
                    language='en',  
                    timestamp=timezone.now()
                )

            # Return both messages in the response
            # the name has to be the SAME as the fetched chat history parameter names in the frontend js file
            # orelse a lot of frontend functions will not work, because this is the jsonresponse that the
            # frontend will get and it access each key by its exact name
            return JsonResponse({
                # accesing values from the user_message and ai_message using keys
                'messages': [
                    {
                        'message_id': user_message.message_id,
                        'sender__username': user.username,
                        'recipient__username': ai, 
                        'message_text': user_message.message_text,
                        'timestamp': user_message.timestamp
                    },
                    {
                        'message_id': ai_message.message_id,
                        'sender__username': ai.username,
                        'recipient__username': user.username,
                        'message_text': ai_message.message_text,
                        'timestamp': ai_message.timestamp
                    }
                ]
            })
        # the caught exception is assigned to the variable e, used in the error message
        # raised when data fails form or model field validation
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)

        # raised when any kind of exception that occurs in the post method. 
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': 'Could not process your message.' + str(e)}, status=500)