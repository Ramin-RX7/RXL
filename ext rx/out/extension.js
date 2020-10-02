"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;

const vscode = require("vscode");
const path = require("path");








function activate(context) {
    console.log('RX Language extension has been successfully activated');
    






    let TEST = vscode.commands.registerCommand('extension.TEST', run);



    context.subscriptions.push(TEST);



}



function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

async function run(){
        //vscode.window.showInformationMessage('RX Language extension has been successfully activated');
        let editor = vscode.window.activeTextEditor;
        editor.document.save();
        if (!editor){
            vscode.window.showErrorMessage('No Open Editor');
            return;
        }
        var terminal = vscode.window.activeTerminal;
        if (terminal){
            changeDirectory();
        }
        else{
            create_terminal_currentdir();
            await sleep(2000);
        }
        terminal = vscode.window.activeTerminal;
        let FN = path.basename(editor.document.fileName);
        terminal.sendText(`\x03python -m RX ${FN}`,true);
}


function followEditorChange() {
    if (vscode.workspace.getConfiguration("terminalSync").get("followActiveEditor", false)) {
        changeDirectory();
    }
}

function changeDirectory() {
    var _a, _b;
    let uri = (_b = (_a = vscode.window.activeTextEditor) === null || _a === void 0 ? void 0 : _a.document) === null || _b === void 0 ? void 0 : _b.uri;
    let terminal = vscode.window.activeTerminal;
    if (uri && terminal) {
        terminal.sendText(`\x03 ${path.dirname(uri.fsPath).slice(0,2)}`, true);
        terminal.sendText(`cd "${path.dirname(uri.fsPath)}"`, true);
    }
}
function create_terminal_currentdir(){
    let terminal = vscode.window.activeTerminal;
    if (!terminal){
        let editor = vscode.window.activeTextEditor;
        let FN = path.dirname(editor.document.fileName); //.uri.fsPath
        
        let terminal = vscode.window.createTerminal( {cwd:FN} );
        terminal.show(false);
    }
}




let ShowSelectedText = vscode.commands.registerCommand('extension.ShowSelectedText', () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor){
        vscode.window.showErrorMessage('Editor Does not Exists');
        return
    }
    const text = editor.document.getText(editor.selection)
    if (!text){
        vscode.window.showErrorMessage('No Selected Word(s) Found');
        return
    }
    vscode.window.showInformationMessage('Selected Text:  '+text);
});


















exports.activate = activate;
// this method is called when your extension is deactivated
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map