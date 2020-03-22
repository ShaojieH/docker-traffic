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
    });
