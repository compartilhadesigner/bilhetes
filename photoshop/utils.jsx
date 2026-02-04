function findLayerSet(parent, name) {
    for (var i = 0; i < parent.layerSets.length; i++) {
        if (parent.layerSets[i].name === name) {
            return parent.layerSets[i];
        }
    }
    return null;
}

function findTextLayer(parent, name) {
    for (var i = 0; i < parent.artLayers.length; i++) {
        var layer = parent.artLayers[i];
        if (layer.name === name && layer.kind === LayerKind.TEXT) {
            return layer;
        }
    }
    return null;
}

function replaceImageInGroup(group, imageFile) {
    if (!imageFile.exists) {
        throw new Error("Imagem não encontrada: " + imageFile.fsName);
    }

    app.open(imageFile);
    var imgDoc = app.activeDocument;

    imgDoc.selection.selectAll();
    imgDoc.selection.copy();
    imgDoc.close(SaveOptions.DONOTSAVECHANGES);

    app.activeDocument = app.documents[0];
    app.activeDocument.activeLayer = group;

    app.activeDocument.paste();
}
