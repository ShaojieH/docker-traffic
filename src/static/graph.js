var selected_id = null;
var is_selected = false;
var selected_name = "";

function showSnackBar(message) {
    var x = document.getElementById("snackbar");
    x.className = "show";
    x.textContent = message;
    setTimeout(function () {
        x.className = x.className.replace("show", "");
    }, 1000);
}

fetch('/api/container_info')
    .then(response => response.json())
    .then(data => {
        console.log(data);
        var cy = window.cy = cytoscape({

            container: document.getElementById('cy'), // container to render in
            elements: data,
            style: [ // the stylesheet for the graph
                {
                    selector: 'node',
                    style: {
                        'background-color': '#1b87cf',
                        'label': 'data(name)'
                    }
                },
                {
                    selector: 'edge',
                    style: {
                        'width': 10,
                        'line-color': '#ccc',
                        'target-arrow-color': '#ccc',
                        'target-arrow-shape': 'triangle',
                        'curve-style': 'bezier',
                        'content': 'data(limit)'
                    }
                }
            ],
            layout: {
                name: 'circle',
            }

        });

        cy.on('tap', 'node', function (evt) {
            console.log('clicked ' + this.id());
            if (is_selected) {
                if (selected_id === this.id()) {
                    is_selected = false;
                    showSnackBar("已取消选择起始节点");
                } else {
                    // selected dst node
                    showSnackBar("已选择结束节点 " + this.data("name"));
                    bootbox.prompt({
                        title:
                            "输入限制速率 <br>" + selected_name + "  =>  " + this.data("name"),
                        callback: function (result) {
                            console.log(result);
                            showSnackBar("添加失败");
                            is_selected = false;
                        },
                        size: "xl"
                    });
                }
            } else {
                is_selected = true;
                selected_id = this.id();
                selected_name = this.data("name");  // TODO save this directly
                showSnackBar("已选择起始节点 " + this.data("name"));
            }
        });
    });
