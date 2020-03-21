fetch('/api/container_info')
    .then(response => response.json())
    .then(data => Object.keys(data))
    .then(container_ids => container_ids.map(
        container_id => {
            return {data: {id: container_id}};
        }
    ))
    .then(data => {
        var cy = window.cy = cytoscape({

            container: document.getElementById('cy'), // container to render in
            elements: data,
            style: [ // the stylesheet for the graph
                {
                    selector: 'node',
                    style: {
                        'background-color': '#1b87cf',
                        'label': 'data(id)'
                    }
                },
                {
                    selector: 'edge',
                    style: {
                        'width': 3,
                        'line-color': '#ccc',
                        'target-arrow-color': '#ccc',
                        'target-arrow-shape': 'triangle'
                    }
                }
            ],
            layout: {
                name: 'circle',
            }

        });
    });
