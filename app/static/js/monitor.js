if (!window.WebSocket) {
    window.WebSocket = window.MozWebSocket;
}

//1.定义长连接
let conn = null;

//进度条变化
function progress_status(val) {
    let data = "";
    if (val >= 0 && val < 25) {
        data = " bg-success";
    } else if (val >= 25 && val < 50) {
        data = "";
    } else if (val >= 50 && val < 75) {
        data = " bg-warning";
    } else if (val >= 75 && val <= 100) {
        data = " bg-success";
    }
    return data
}

//连接提示信息
function log(cls, msg) {
    document.getElementById("monitor_status").innerHTML = "<div class='alert alert-" + cls + "'>" + msg + "</div>";
}

//专门实时更新信息
function update_ui(e) {
    let data = e.data;
    data = JSON.parse(data); //把json字符串转化为对象
    /*平均CPU*/
    option_cpu_avg.series[0].data[0] = (data['cpu']['percent_avg'] / 100).toFixed(4);
    option_cpu_avg.title[0].text = data['dt'] + "-CPU平均使用率";
    chart_cpu_avg.setOption(option_cpu_avg);
    /*单独CPU*/
    let cpu_per = "";
    for (let k in data['cpu']['percent_per']) {
        let num = parseInt(k);
        cpu_per += "<tr><td class='text-primary' style='width: 30%'>CPU" + num + "</td>";
        cpu_per += "<td><div class='progress'><div class='progress-bar progress-bar-striped progress-bar-animated" + progress_status(data['cpu']['percent_per'][k]) + "' role='progressbar' aria-valuenow='" + data['cpu']['percent_per'][k] + "' aria-valuemin='0' aria-valuemax='100' style='width: " + data['cpu']['percent_per'][k] + "%'>" + data['cpu']['percent_per'][k] + "%</div></div></td></tr>";
    }
    document.getElementById("tb_cpu_per").innerHTML = cpu_per;
    /*内存实时更新*/
    option_mem.series[0].data[0].value = data['mem']['percent'];
    option_mem.title[0].text = data["dt"] + "-内存使用率";
    chart_mem.setOption(option_mem);
    document.getElementById("mem_percent").innerText = data['mem']['percent'];
    document.getElementById("mem_total").innerText = data['mem']['total'];
    document.getElementById("mem_used").innerText = data['mem']['used'];
    document.getElementById("mem_free").innerText = data['mem']['free'];

    /*交换分区实时更新*/
    option_swap.series[0].data[0].value = data['swap']['percent'];
    option_swap.title[0].text = data["dt"] + "-交换分区使用率";
    chart_swap.setOption(option_swap);
    document.getElementById("swap_percent").innerText = data['swap']['percent'];
    document.getElementById("swap_total").innerText = data['swap']['total'];
    document.getElementById("swap_used").innerText = data['swap']['used'];
    document.getElementById("swap_free").innerText = data['swap']['free'];

    /*网络信息更新*/
    let net = "";
    for (let k in data['net']) {
        let cd = data['net'][k];
        if (parseInt(cd['bytes_sent']) != 0 && parseInt(cd["bytes_recv"]) != 0) {
            let index = parseInt(k) + 1;
            let op = eval("option_net" + index);
            let ch = eval("chart_net" + index);
            op.title[0].text = data["dt"] + "-" + cd["name"] + "网卡信息";
            op.series[0].data = [
                {"name": "收包数", "value": cd["packets_recv"]},
                {"name": "发包数", "value": cd["packets_sent"]}
            ];
            op.series[1].data = [
                {"name": "收字节", "value": cd["bytes_recv"]},
                {"name": "发字节", "value": cd["bytes_sent"]}
            ];
            ch.setOption(op);
        }
        net += "<tr><td>" + cd['name'] + "</td>";
        net += "<td class='text-danger'>" + cd['bytes_sent'] + "</td>";
        net += "<td class='text-danger'>" + cd['bytes_recv'] + "</td>";
        net += "<td class='text-danger'>" + cd['packets_sent'] + "</td>";
        net += "<td class='text-danger'>" + cd['packets_recv'] + "</td>";
        net += "<td>" + cd['family'] + "</td>";
        net += "<td>" + cd['address'] + "</td>";
        net += "<td>" + cd['netmask'] + "</td>";
        if (cd['broadcast']) {
            net += "<td>" + cd['broadcast'] + "</td></tr>";
        } else {
            net += "<td>无</td></tr>";
        }
    }
    document.getElementById("tb_net").innerHTML = net;

    /*磁盘使用信息实时更新*/
    let disk = "";
    for (let k in data["disk"]) {
        let cd = data["disk"][k];
        disk += "<tr><td>" + cd['device'] + "</td>";
        disk += "<td>" + cd['mountpoint'] + "</td>";
        disk += "<td>" + cd['fstype'] + "</td>";
        disk += "<td>" + cd['opts'] + "</td>";
        disk += "<td class='text-danger'>" + cd['used']['total'] + "GB</td>";
        disk += "<td class='text-danger'>" + cd['used']['used'] + "GB</td>";
        disk += "<td class='text-danger'>" + cd['used']['free'] + "GB</td>";
        disk += "<td><div class='progress'><div class='progress-bar progress-bar-striped progress-bar-animated" + progress_status(cd['used']['percent']) + "' role='progressbar' aria-valuenow='" + cd['used']['percent'] + "' aria-valuemin='0' aria-valuemax='100' style='width: " + cd['used']['percent'] + "%'>" + cd['used']['percent'] + "%</div></div></td></tr>";
    }
    document.getElementById("tb_disk").innerHTML = disk;
}

//2.定义连接函数
function connect() {
    disconnect();//把之前没关闭的连接关闭掉，再创建新的连接
    //创建连接对象
    conn = new WebSocket(`ws://${window.location.host}/real/time/`);
    log("warning", "正在连接....");
    //建立连接
    conn.onopen = function () {
        console.log("连接成功！");
        log("success", "连接成功！");
    };
    //建立接受消息
    conn.onmessage = function (e) {
        //console.log(e.data)
        update_ui(e);
    };
    //建立关闭连接
    conn.onclose = function () {
        console.log("连接断开！");
        log("danger", "连接断开！");
    };
    //每隔几秒触发一个事件
    setInterval(function () {
        conn.send("system");
    }, 500);
}

//3.定义断开连接函数
function disconnect() {
    if (conn != null) {
        log("danger", "连接断开！");
        conn.close(); //关闭连接
        conn = null;
    }
}

//4.刷新页面时候，断开连接，重新连接，断线重连判断
if (conn == null) {
    connect()
} else {
    disconnect();
}
