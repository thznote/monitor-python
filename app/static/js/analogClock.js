function AnalogClockOption(width, foreColor, bgColor) {
    this.foreColor = foreColor ? foreColor : "#000";
    this.bgColor = bgColor ? bgColor : "#eee";
    this.width = width ? width : 400;
}

function AnalogClock(id, option) {

    let dateTimeFormat = function (time) {
        let str = "";
        str += time.getYear() + (time.getYear() > 1900 ? 0 : 1900) + "-";
        str += time.getMonth() + 1 + "-";
        str += time.getDate() + "<br/> ";
        str += time.getHours() + ":";
        str += time.getMinutes() + ":";
        str += time.getSeconds();
        return str;
    };

    if (!option)
        option = {};
    this.foreColor = option.foreColor ? option.foreColor : "#000";
    this.bgColor = option.bgColor ? option.bgColor : "#eee";
    this.width = option.width ? option.width : 400;

    this.container = document.getElementById(id);
    if (!this.container)
        return;
    this.container.style.fontcolor = this.foreColor;

    this.panel = document.createElement("div");
    this.panel.style.borderRadius = "50%";
    this.panel.style.backgroundColor = this.bgColor;
    this.panel.style.border = "solid 1px #ccc";
    this.panel.style.width = this.width + "px";
    this.panel.style.height = this.width + "px";
    this.panel.style.position = "relative";
    this.panel.style.marginLeft = "auto";
    this.panel.style.marginRight = "auto";
    this.container.appendChild(this.panel);

    let label = document.createElement("h4");
    label.style.width = "100%";
    label.style.textAlign = "center";
    label.style.fontWeight = "normal";
    label.style.fontSize = this.width / 15 + "px";
    label.style.marginTop = this.width * 0.6 + "px";
    label.style.color = this.foreColor;
    label.innerHTML = dateTimeFormat(new Date());
    if (this.width >= 100)
        this.panel.appendChild(label);

    let ul = document.createElement("ul");
    ul.style.height = "100%";

    ul.style.padding = "0";
    ul.style.margin = "0";
    ul.style.listStyle = "none";
    ul.style.position = "absolute";
    ul.style.width = 40 + "px";
    ul.style.top = 0;
    ul.style.left = this.width / 2 - 20 + "px";
    ul.style.color = this.foreColor;
    this.panel.appendChild(ul);

    for (let i = 0; i <= 5; i++) {
        if (!localStorage)
            break;

        let list = document.createElement("li");
        list.style.padding = "0";
        list.style.margin = "0";
        list.style.position = "absolute";
        list.style.textAlign = "center";
        list.style.width = "40px";
        list.style.height = this.width + "px";
        list.style.fontSize = this.width / 10 + "px";
        ul.appendChild(list);

        list.style.transform = "rotate(" + 360 / 12 * (i + 1) + "deg)";

        let numTop = document.createElement("div");
        numTop.style.width = "100%";
        numTop.style.position = "absolute";
        numTop.style.textAlign = "center";
        numTop.innerHTML = i + 1;
        if (this.width < 100)
            numTop.innerHTML = "●";
        list.appendChild(numTop);

        numTop.style.transform = "rotate(" + -360 / 12 * (i + 1) + "deg)";

        let numBottom = document.createElement("div");
        numBottom.style.width = "100%";
        numBottom.style.position = "absolute";
        numBottom.style.textAlign = "center";
        numBottom.style.bottom = "0";
        numBottom.innerHTML = i + 7;
        if (this.width < 100)
            numBottom.innerHTML = "●";
        list.appendChild(numBottom);

        numBottom.style.transform = "rotate(" + -360 / 12 * (i + 1) + "deg)";
    }

    let hour = document.createElement("div");
    let hourWidth = this.width * 0.02;
    let hourTop = this.width * 0.25 - (hourWidth * 0.5);
    let hourleft = this.width * 0.5 - hourWidth * 0.5;
    hour.style.width = hourWidth + "px";
    hour.style.height = hourWidth + "px";
    hour.style.position = "absolute";
    hour.style.border = "solid 0px transparent";
    hour.style.left = hourleft + "px";
    hour.style.top = hourTop + "px";
    hour.style.borderTop = "solid " + (this.width * 0.5 - hourTop) + "px #f60";
    hour.style.borderBottomWidth = (this.width * 0.5 - hourTop) + "px";
    if (localStorage)
        this.panel.appendChild(hour);

    let min = document.createElement("div");
    let minWidth = this.width * 0.01;
    let minTop = this.width * 0.1 - (minWidth * 0.5);
    let minleft = this.width * 0.5 - minWidth * 0.5;
    min.style.width = minWidth + "px";
    min.style.height = minWidth + "px";
    min.style.position = "absolute";
    min.style.border = "solid 0px transparent";
    min.style.left = minleft + "px";
    min.style.top = minTop + "px";
    min.style.borderTop = "solid " + (this.width * 0.5 - minTop) + "px #09f";
    min.style.borderBottomWidth = (this.width * 0.5 - minTop) + "px";
    if (localStorage)
        this.panel.appendChild(min);

    let sec = document.createElement("div");
    let secWidth = 1;
    let secTop = this.width * 0.05;
    sec.style.width = secWidth + "px";
    sec.style.height = secWidth + "px";
    sec.style.position = "absolute";
    sec.style.border = "solid 0px transparent";
    sec.style.left = (this.width * 0.5 - secWidth) + "px";
    sec.style.top = secTop + "px";
    sec.style.borderTop = "solid " + (this.width * 0.5 - secTop) + "px " + this.foreColor;
    sec.style.borderBottomWidth = (this.width * 0.5 - secTop) + "px";
    if (localStorage)
        this.panel.appendChild(sec);

    let point = document.createElement("div");
    let pointWidth = this.width * 0.05;
    point.style.width = pointWidth + "px";
    point.style.height = pointWidth + "px";
    point.style.position = "absolute";
    point.style.backgroundColor = this.foreColor;
    point.style.left = this.width * 0.5 - (pointWidth * 0.5) + "px";
    point.style.top = this.width * 0.5 - (pointWidth * 0.5) + "px";
    point.style.borderRadius = "50%";
    if (localStorage)
        this.panel.appendChild(point);

    this.loop = setInterval(function () {
        let now = new Date();
        label.innerHTML = dateTimeFormat(now);

        let roS = 1.0 * 360 / 60 * now.getSeconds();
        let roM = 1.0 * 360 / 60 * now.getMinutes();
        let roH = 1.0 * 360 / 12 * (now.getHours() % 12) + 1.0 * 360 / 12 * (now.getMinutes() / 60);

        sec.style.transform = 'rotate(' + roS + 'deg)';
        min.style.transform = 'rotate(' + roM + 'deg)';
        hour.style.transform = 'rotate(' + roH + 'deg)';
    }, 1000);
}
