function bargraph(id, data, labels = null, len = null) {
    if (labels == null) {
        labels = [];
        for (let i = 0; i < data.length; i++) {
            labels.push(i)
        }
    }
    let svgHeight = 500;
    let svgWidth = 1000;
    let svg = document.getElementById(id);

    if (svg == null) {
        console.log("ERROR: couldn't find svg with id " + id);
        return;
    }
    let max = -1 * Infinity;
    for (let i = 0; i < data.length; i++) {
        if (data[i] > max) {
            max = data[i]
        }
    }
    if (max <= 0) {
        //won't work for graphing negative values
        //return
        max=1
    } else {
        //we have data, make the svg take up more than 0px
        //svg.style.height = svgHeight;
        //svg.style.width = svgWidth;
    }
    let width;
    let fontSize = 14;
    if (len == null) {
        width = (svgWidth - fontSize * 2) / data.length;
    } else {
        width = (svgWidth - fontSize * 2) / len;
    }
    let graphHeight = svgHeight - fontSize;
    let currY = graphHeight;
    let increment = 10;
    for (let i = 0; i < increment; i++) {
        let line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttributeNS(null, "x1", 0);
        line.setAttributeNS(null, "y1", currY);
        line.setAttributeNS(null, "x2", svgWidth);
        line.setAttributeNS(null, "y2", currY);
        line.setAttributeNS(null, "stroke-width", "1");
        line.setAttributeNS(null, "stroke", "black");
        svg.appendChild(line);

        let text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttributeNS(null, "x", 0);
        text.setAttributeNS(null, "y", currY + fontSize / 2);
        text.setAttributeNS(null, "font-size", fontSize);
        let label = document.createTextNode((i * (max / increment)).toFixed(3));
        text.appendChild(label);
        svg.appendChild(text);
        currY -= graphHeight / increment;
    }
    let currX = fontSize * 2;
    for (let i = 0; i < data.length; i++) {
        let rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        rect.setAttributeNS(null, "x", currX);
        rect.setAttributeNS(null, "y", graphHeight - (graphHeight * data[i] / max)); //y will be kinda inverted for now
        rect.setAttributeNS(null, "width", width*.8);
        rect.setAttributeNS(null, "height", graphHeight * data[i] / max);
        rect.setAttributeNS(null, "class", "bargraph-bar");
        svg.appendChild(rect);
        let text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttributeNS(null, "x", currX);
        text.setAttributeNS(null, "y", graphHeight + fontSize);
        text.setAttributeNS(null, "font-size", fontSize);
        let content = document.createTextNode(labels[i]);
        text.appendChild(content);
        svg.appendChild(text);
        currX += width;
    }
}