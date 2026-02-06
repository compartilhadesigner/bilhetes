#target photoshop
#include "utils.jsx"
#include "prototypes.jsx"

function save_images() {
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

    hideAllGroups(doc);

    function saveForWebPNG(file) {
        var options = new ExportOptionsSaveForWeb();
        options.format = SaveDocumentType.PNG;
        options.PNG8 = false;                 // PNG-24
        options.transparency = true;          // manter transparência
        options.interlaced = false;
        options.includeProfile = true;        // incorporar perfil de cores
        options.convertToSRGB = true;         // converter para sRGB
        options.optimized = true;

        doc.exportDocument(file, ExportType.SAVEFORWEB, options);
    }

    for (var i = 0; i < doc.layerSets.length; i++) {
        var customerGroup = doc.layerSets[i];

        customerGroup.visible = true;

        var file = new File(outputFolder + "/" + customerGroup.name + ".png");
        saveForWebPNG(file);

        customerGroup.visible = false;
    }

    alert("Exportação PNG-24 (Save for Web) concluída.");
}

save_images()