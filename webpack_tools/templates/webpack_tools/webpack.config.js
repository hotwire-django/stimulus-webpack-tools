const webpack = require('webpack');
const glob = require('glob');
const TerserPlugin = require('terser-webpack-plugin')


let globOptions = {
    ignore: ['node_modules/**', 'venv/**']
}

let entryFiles = glob.sync("**/javascript/*.js", globOptions)

let entryObj = {}

entryFiles.forEach(function(file){
    if (file.includes('.')) {
        let parts = file.split('/')
        let path = parts.pop()
        let fileName = path.split('.')[0];
        entryObj[fileName] = `./${file}`;
    }
})

const optimize = {
    production: {
        usedExports: true,
        minimize: true
    },
    development: {
        minimize: false
    }
}

// const mode = 'production'
const mode = 'development'

// const babel = {
//     presets: [
//         '@babel/preset-env'
//     ],
//     plugins: [
//         '@babel/plugin-proposal-class-properties'
//     ]
// }

// https://medium.com/@craigmiller160/how-to-fully-optimize-webpack-4-tree-shaking-405e1c76038

const babel = {
    env: {
        development: {
            presets: [
                '@babel/preset-env'
            ]
        },
        production: {
            presets: [
                '@babel/preset-env'
            ]
        }
    },
    plugins: [
        [ "@babel/plugin-proposal-decorators", {
            legacy: true,
        } ],
        [ "@babel/plugin-proposal-class-properties", { "loose": true } ],
        [ "@babel/plugin-transform-runtime"]
    ]
}

const config = {
    // mode: process.env.NODE_ENV,
    mode: mode,
    entry: entryObj,
    output: {
        path: __dirname + '/static/js',
        filename: '[name].js'
    },
    target: "browserslist:last 2 Chrome versions",
    // NOTE: Webpack 5 has major architectural improvements regarding targets and different kinds of imports, but they're not fully implemented yet. The following line is a workaround and should be removed when the features are complete. https://webpack.js.org/blog/2020-10-10-webpack-5-release/#improved-target-option
    externalsPresets: { web: false, webAsync: true },
    optimization: optimize[mode],
    cache: false,
    resolve: {
        preferRelative: true,
        alias: {
            "jquery": "blackstone-ui/helpers/backbone/jquery-shim",
            "bui": "blackstone-ui"
        }
    },
    module: {
        rules: [
            {
                test: /\.less$/,
                use: [
                    'style-loader',
                    'css-loader',
                    'less-loader'
                ]
            },
            {
                test: /\.svg(\.html)?$/,
                use: {
                    loader: 'file-loader',
                    options: {
                        name: "[name].[ext]",
                        outputPath: 'images',
                        publicPath: './images/'
                    }
                },
            },
            {
                test: /\.js/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: babel
                }
            }
        ],
    }
}

module.exports = config