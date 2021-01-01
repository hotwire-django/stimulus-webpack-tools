import { Application } from "stimulus"
import { definitionsFromContext } from "stimulus/webpack-helpers"

// DO NOT REMOVE THIS AND THE FOLLOWING LINE
// Custom Controller Imports

// This file automatically initialised by stimulus-webpack-helper
const application = Application.start()
const context = require.context("./controllers", true, /\.js$/)
application.load(definitionsFromContext(context))

// DO NOT REMOVE THIS AND THE FOLLOWING LINE
// Custom Controllers
