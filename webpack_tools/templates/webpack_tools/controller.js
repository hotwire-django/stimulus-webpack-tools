// Controller: {{ name }}
import { Controller } from "stimulus";

// This file automatically initialised by stimulus-webpack-helper
export default class extends Controller {

    connect() {
        console.log("Hello Stimulus from Controller {{ name }}: ", this.element)
    }

}