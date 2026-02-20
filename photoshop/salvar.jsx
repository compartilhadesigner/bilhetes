#target photoshop
#include "utils.jsx"
#include "prototypes.jsx"

function save_image(customerName, index) {

    if (!app.documents.length) {
        alert("Abra o PSD antes de rodar o script.");
        return;
    }

    var doc = app.activeDocument;

    var scriptFolder = new File($.fileName).parent;

    var outputFolder = new Folder(scriptFolder + "/output");
    if (!outputFolder.exists) {
        outputFolder.create();
    }

    function hideAllGroups(parent) {
        for (var i = 0; i < parent.layerSets.length; i++) {
            parent.layerSets[i].visible = false;
        }
    }

    function saveForWebPNG(file) {
        var options = new ExportOptionsSaveForWeb();
        options.format = SaveDocumentType.PNG;
        options.PNG8 = false;      
        options.transparency = true;
        options.interlaced = false;
        options.includeProfile = true;
        options.convertToSRGB = true;
        options.optimized = true;

        doc.exportDocument(file, ExportType.SAVEFORWEB, options);
    }

    // 🔥 1. Oculta tudo
    hideAllGroups(doc);

    // 🔥 2. Procura o grupo do customer
    var customerGroup = null;

    for (var i = 0; i < doc.layerSets.length; i++) {
        if (doc.layerSets[i].name === customerName) {
            customerGroup = doc.layerSets[i];
            break;
        }
    }

    if (!customerGroup) {
        alert("Grupo do customer não encontrado: " + customerName);
        return;
    }

    // 🔥 3. Ativa somente ele
    customerGroup.visible = true;

    // 🔥 4. Salva uma única imagem
    var file = new File(outputFolder + "/" + customerName + "_" + index.toString() + ".png");
    saveForWebPNG(file);
}
