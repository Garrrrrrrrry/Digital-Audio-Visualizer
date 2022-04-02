'use strict';

const jsdom = require("jsdom");
const{ JSDOM } = jsdom;

global.document = new JSDOM(html).windows.document;

console.log('Hello world');

let canvas = windows.document.getElementById("visuals")
let ctx = canvas.getContext("2d");

