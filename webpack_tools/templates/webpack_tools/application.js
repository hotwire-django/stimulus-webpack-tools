import { Application } from "stimulus"
import { definitionsFromContext } from "stimulus/webpack-helpers"

// This file automatically initialised by stimulus-webpack-helper
const application = Application.start()
const context = require.context("./controllers", true, /\.js$/)
application.load(definitionsFromContext(context))