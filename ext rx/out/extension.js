"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;

const vscode = require("vscode");
const path = require("path");

















// {!!!}
function followEditorChange() {
    if (vscode.workspace.getConfiguration("terminalSync").get("followActiveEditor", false)) {
        changeDirectory();
    }
}










// Run RX File
async function run(){
    //vscode.window.showInformationMessage('RX Language extension has been successfully activated');
    
    let editor = vscode.window.activeTextEditor;
    if (editor && !editor.document.isUntitled) {editor.document.save();}
    
    var terminal = vscode.window.activeTerminal;
    if (terminal){
        changeDirectory();
    }
    else{
        create_terminal_currentdir();
        await sleep(2000);
    }
    var terminal = vscode.window.activeTerminal;
    if (editor && !editor.document.isUntitled){
        //let FN = path.basename(editor.document.fileName);
        terminal.sendText(`\x03python -m RX ${path.basename(editor.document.fileName)}`,true);
    }
    else {
        terminal.sendText(`\x03python -m RX`,true);
    }
}
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
function changeDirectory() {
    var editor = vscode.window.activeTextEditor
    var terminal = vscode.window.activeTerminal;
    var _a, _b;
    let uri = (_b = (_a = vscode.window.activeTextEditor) === null || _a === void 0 ? void 0 : _a.document) === null || _b === void 0 ? void 0 : _b.uri;
    if (uri && terminal && editor && !editor.document.isUntitled) {
        terminal.sendText(`\x03 ${path.dirname(uri.fsPath).slice(0,2)}`, true);
        terminal.sendText(`cd "${path.dirname(uri.fsPath)}"`, true);
      }
}
function create_terminal_currentdir(){
    var terminal = vscode.window.activeTerminal;
    if (!terminal){
        var editor = vscode.window.activeTextEditor;
        if (editor && !editor.document.isUntitled){
            var FN = path.dirname(editor.document.fileName); //.uri.fsPath
            return false;
        }
        else {var FN = 'C:\\'}
        
        var terminal = vscode.window.createTerminal( {cwd:FN} );
        terminal.show(false);
    }
}
var Run = vscode.commands.registerCommand('extension.run', run)



// Show Selected Text
function show_selected_text() {
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
};
var ShowSelectedText = vscode.commands.registerCommand('extension.ShowSelectedText', show_selected_text)

// {USEFULL}

/*
var editor = vscode.window.activeTextEditor
//] ACTIVE FILE
editor.document.fileName                // Abspath
editor.document.getText()               // Content
editor.document.isUntitled              // Abspath
editor.document.languageId              // Language ID
editor.document.lineAt(3).text          // Get Text of line 3+1 (index 3)
editor.document.lineCount.toString()    // Line Numbers
editor.viewColumn.toString()            // In which Column
*/












function activate(context) {
    console.log('RX Language extension has been successfully activated');
    





    function Test(){
    
        var editor = vscode.window.activeTextEditor;
        //var X = editor.selection;
        //vscode.window.showErrorMessage(X)
    }


    let TEST = vscode.commands.registerCommand('extension.TEST', Test);
    context.subscriptions.push(TEST);








}




















exports.activate = activate;
// this method is called when your extension is deactivated
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map