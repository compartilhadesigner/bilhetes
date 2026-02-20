#include "json2.js"

function readDataFile(fileName) {

    var scriptFile = new File($.fileName);
    var scriptFolder = scriptFile.parent;

    var dataFile = new File(scriptFolder.parent + "/" + fileName);

    if (!dataFile.exists) {
        throw new Error("Arquivo " + fileName + " não encontrado.");
    }

    dataFile.open("r");
    var content = dataFile.read();
    dataFile.close();

    if (!content) {
        throw new Error("Arquivo JSON vazio.");
    }

    if (typeof JSON === "undefined") {
        throw new Error("JSON não disponível nesta versão do ExtendScript.");
    }

    return JSON.parse(content);
}