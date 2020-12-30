/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/
define(["require", "exports", "vs/base/common/event"], function (require, exports, event_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    class ColorPickerModel {
        constructor(color, availableColorPresentations, presentationIndex) {
            this.presentationIndex = presentationIndex;
            this._onColorFlushed = new event_1.Emitter();
            this.onColorFlushed = this._onColorFlushed.event;
            this._onDidChangeColor = new event_1.Emitter();
            this.onDidChangeColor = this._onDidChangeColor.event;
            this._onDidChangePresentation = new event_1.Emitter();
            this.onDidChangePresentation = this._onDidChangePresentation.event;
            this.originalColor = color;
            this._color = color;
            this._colorPresentations = availableColorPresentations;
        }
        get color() {
            return this._color;
        }
        set color(color) {
            if (this._color.equals(color)) {
                return;
            }
            this._color = color;
            this._onDidChangeColor.fire(color);
        }
        get presentation() { return this.colorPresentations[this.presentationIndex]; }
        get colorPresentations() {
            return this._colorPresentations;
        }
        set colorPresentations(colorPresentations) {
            this._colorPresentations = colorPresentations;
            if (this.presentationIndex > colorPresentations.length - 1) {
                this.presentationIndex = 0;
            }
            this._onDidChangePresentation.fire(this.presentation);
        }
        selectNextColorPresentation() {
            this.presentationIndex = (this.presentationIndex + 1) % this.colorPresentations.length;
            this.flushColor();
            this._onDidChangePresentation.fire(this.presentation);
        }
        guessColorPresentation(color, originalText) {
            for (let i = 0; i < this.colorPresentations.length; i++) {
                if (originalText === this.colorPresentations[i].label) {
                    this.presentationIndex = i;
                    this._onDidChangePresentation.fire(this.presentation);
                    break;
                }
            }
        }
        flushColor() {
            this._onColorFlushed.fire(this._color);
        }
    }
    exports.ColorPickerModel = ColorPickerModel;
});
//# sourceMappingURL=colorPickerModel.js.map