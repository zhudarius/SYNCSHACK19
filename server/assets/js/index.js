$(document).ready(() => {
    console.log("Ready!");

    initialise_graph();
});

// Send a POST request
axios({
    method: 'POST',
    url: 'http://10.42.0.50:5000/unit_category',
    data: {
        units_taken: ["C", "D"]
    }
})
    .then(res => {
        res.data = JSON.parse(res.data.replace(/'/g, '"'))
        console.log(res.data);
    })
    .catch(err => {
        console.log(err);
    });


// axios.get("http://10.42.0.50:5000/unit_category")
//     .then(res => {
//         console.log(res.data);

//         // $("h2")[0].innerHTML =
//         //     `<ul>`
//         //     +
//         //     res.data.map((x) => `<li>` + x.data.testKey + `</li>`).join("")
//         //     +
//         //     `</ul>`;

//     })
//     .catch(err => {
//         console.log(err);
//     })


function full_screen(e) {
    console.log("HI");
    $("#graph_div").toggleClass("full_screen_graph");
    initialise_graph();
}

function initialise_graph() {
    // return;

    $("#cy").innerHTML = "";
    var cy = cytoscape({
        container: $('#cy'),

        elements: [ // list of graph elements to start with
            { // node a
                data: { id: 'a' }
            },
            { // node b
                data: { id: 'b' }
            },
            { // edge ab
                data: { id: 'ab', source: 'a', target: 'b' }
            }
        ],

        style: [ // the stylesheet for the graph
            {
                selector: 'node',
                style: {
                    'background-color': '#666',
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
            name: 'grid',
            rows: 1
        },

        wheelSensitivity: 0.2,
        minZoom: 0.5,
        maxZoom: 3
    });
}