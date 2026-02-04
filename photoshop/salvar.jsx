#target photoshop

(function () {
    if (!app.documents.length) {
        alert("Abra o PSD antes de rodar o script.");
        return;
    }

    var doc = app.activeDocument;

    // Pasta onde está o script
    var scriptFolder = new File($.fileName).parent;

    // Pasta de saída
    var outputFolder = new Folder(scriptFolder + "/output");
    if (!outputFolder.exists) {
        outputFolder.create();
    }

    // Esconde todas as pastas
    function hideAllGroups(parent) {
        for (var i = 0; i < parent.layerSets.length; i++) {
            parent.layerSets[i].visible = false;
        }
    }

    hideAllGroups(doc);

    // Configuração Save for Web (PNG-24)
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

    // Percorre cada pasta de customer
    for (var i = 0; i < doc.layerSets.length; i++) {
        var customerGroup = doc.layerSets[i];

        // Mostra apenas a pasta atual
        customerGroup.visible = true;

        var file = new File(outputFolder + "/" + customerGroup.name + ".png");
        saveForWebPNG(file);

        // Esconde novamente
        customerGroup.visible = false;
    }

    alert("Exportação PNG-24 (Save for Web) concluída.");
})();
