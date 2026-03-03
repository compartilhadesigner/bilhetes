function toFloat(value) {
    if (typeof value === "number") {
        return value;
    }

    if (typeof value !== "string") {
        return 0;
    }

    value = value.replace(/\s+/g, "");

    value = value.replace(",", ".");

    var num = parseFloat(value);

    return isNaN(num) ? 0 : num;
}


function getLayerCenterPx(layer) {
    var b = layer.bounds; // UnitValue[]
    var left   = b[0].as("px");
    var top    = b[1].as("px");
    var right  = b[2].as("px");
    var bottom = b[3].as("px");

    return {
        x: (left + right) / 2,
        y: (top + bottom) / 2
    };
}

function getLayerBoundsPx(layer) {
    var b = layer.bounds;
    return {
        left:  b[0].as("px"),
        top:   b[1].as("px"),
        right: b[2].as("px"),
        bottom:b[3].as("px")
    };
}

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

function findFirstArtLayer(group) {
    for (var i = 0; i < group.layers.length; i++) {
        if (group.layers[i].typename === "ArtLayer") {
            return group.layers[i];
        }
    }
    return null;
}

function replaceImageInGroup(group, imageFile) {
    if (!imageFile.exists) {
        throw new Error("Imagem não encontrada: " + imageFile.fsName);
    }

    var TARGET_W = 535;
    var TARGET_H = 1278;

    var targetLayer = findFirstArtLayer(group);
    if (!targetLayer) {
        throw new Error("Nenhuma camada de imagem encontrada no grupo.");
    }

    var oldCenter = getLayerCenterPx(targetLayer);

    app.open(imageFile);
    var imgDoc = app.activeDocument;

    imgDoc.selection.selectAll();
    imgDoc.selection.copy();
    imgDoc.close(SaveOptions.DONOTSAVECHANGES);

    var mainDoc = app.documents[0];
    app.activeDocument = mainDoc;

    targetLayer.remove();

    mainDoc.activeLayer = group;
    var newLayer = mainDoc.paste();
    newLayer.move(group, ElementPlacement.INSIDE);

    // -------------------------
    // REDIMENSIONAMENTO PROPORCIONAL
    // -------------------------

    var bounds = newLayer.bounds; // [left, top, right, bottom]

    var width = bounds[2].as("px") - bounds[0].as("px");
    var height = bounds[3].as("px") - bounds[1].as("px");

    var scaleX = TARGET_W / width;
    var scaleY = TARGET_H / height;

    // Usa o maior fator para preencher o máximo possível sem deformar
    var scale = Math.max(scaleX, scaleY) * 100;

    newLayer.resize(scale, scale, AnchorPosition.MIDDLECENTER);

    // -------------------------
    // Re-centraliza
    // -------------------------

    var newCenter = getLayerCenterPx(newLayer);

    var dx = oldCenter.x - newCenter.x;
    var dy = oldCenter.y - newCenter.y;

    newLayer.translate(dx, dy);
}

function formatarMoedaBR(valor) {
    valor = Number(valor);

    if (isNaN(valor)) {
        return "R$0,00";
    }

    // Garante duas casas decimais
    var partes = valor.toFixed(2).split(".");

    var inteiro = partes[0];
    var decimal = partes[1];

    // Adiciona separador de milhar manualmente
    var resultado = "";
    while (inteiro.length > 3) {
        resultado = "." + inteiro.slice(-3) + resultado;
        inteiro = inteiro.slice(0, -3);
    }

    resultado = inteiro + resultado;

    return "R$" + resultado + "," + decimal;
}