const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  mode: 'development', // or 'production' or 'none'
  entry: {
    main: './frontend/src/main.js',
    // Add more entry points as needed
  },
  output: {
    filename: '[name].bundle.js',
    // __dirname is where webpack.config.js lives
    path: path.resolve(__dirname, 'dist'),
    publicPath: '/',
  },
  plugins: [
    // Add more HtmlWebpackPlugin instances for each HTML file
    new HtmlWebpackPlugin({
      template: './frontend/src/main.html',
      filename: 'index.html', // so it's the root url, when $ npm run is ran it'll output this
      chunks: ['main'],
    }),
    new MiniCssExtractPlugin({
      filename: '[name].css',
      chunkFilename: '[id].css',
    }),
  ],
  module: {
    rules: [
      // tell webpack how to handle different types of files
      {
        test: /\.js?$/, 
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react'],
          },
        },
      },
      {
        test: /\.css$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          {
            // remember to npm install postcss-loader and
            // use tailwind css and autoprefixer
            // orelse the tailwind css won't work
            // and main.css won't be applied to the js 
            // and the cssextracter won't work
            // and the css will be broken
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: [
                  require('tailwindcss'),
                  require('autoprefixer'),
                ],
              }
            },
          },
        ],
      },
    ],
  },
  
  resolve: {
    extensions: ['.js', '.jsx'],
  },
  devServer: {
    historyApiFallback: true,
    // ...
  },

};