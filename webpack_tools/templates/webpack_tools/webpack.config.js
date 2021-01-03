// This File was automatically initialized by stimulus-webpack-tools
const webpack = require('webpack');
const glob = require('glob');
const TerserPlugin = require('terser-webpack-plugin')
const path = require('path');


let globOptions = {
    ignore: ['node_modules/**', 'venv/**']
}

let entryFiles = glob.sync("**/javascript/*.js", globOptions)

let entryObj = {}

entryFiles.forEach(function (file) {
    let sep = path.sep
    let parts = file.split(sep)
    // General approach
    // output will be app-root/static/{app-name}/js/{entrypoint-filename}
    let fileName = parts.slice(0, -2).join(sep) + `${sep}static${sep}` + parts[parts.length - 3] + `${sep}js${sep}` + parts[parts.length - 1]
    entryObj[fileName] = `.${sep}${file}`;
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
        ["@babel/plugin-proposal-decorators", {
            legacy: true,
        }],
        ["@babel/plugin-proposal-class-properties", {"loose": true}],
        ["@babel/plugin-transform-runtime"]
    ]
}

const config = {
    // mode: process.env.NODE_ENV,
    mode: mode,
    entry: entryObj,
    output: {
        path: __dirname,
        filename: '[name]'
    },
    target: "browserslist:last 2 Chrome versions",
    // NOTE: Webpack 5 has major architectural improvements regarding targets and different kinds of imports, but they're not fully implemented yet. The following line is a workaround and should be removed when the features are complete. https://webpack.js.org/blog/2020-10-10-webpack-5-release/#improved-target-option
    externalsPresets: {web: false, webAsync: true},
    optimization: optimize[mode],
    cache: false,
    resolve: {
        preferRelative: true,
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
