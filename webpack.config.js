var path = require("path")
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

module.exports = {
  context: __dirname,

  entry: './foosball/gameapp/ui/components/main',

  output: {
      path: path.resolve('./foosball/gameapp/ui/bundles/'),
      filename: "[name]-[hash].js",
  },

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
  ],

  module: {
    loaders: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        loader: 'babel-loader',
        query:
            {
                presets:['es2015', 'react']
            }
      }, // to transform JSX into JS
    ],
  },

  resolve: {
    modules: [
      'node_modules',
      'bower_components',
      'web_modules'
    ],
    extensions: ['.js', '.jsx'],
  },
}
