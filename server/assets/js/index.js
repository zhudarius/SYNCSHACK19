var graph_data;

if (lots_of_data) {
    graph_data = lots_of_data;
}

$(document).ready(() => {
    console.log("Ready!");


    $(window).resize(function () {
        initialise_graph(graph_data);
    });

    $("#course_map").css("left", $("#cy").width() / 2);
    $("#course_map").css("transform", "translateX(-50%)");
    $("#course_map").css("transform", "translateY(25px)");


    load_data(graph_data);
});

function stretch_units_list() {
    var list = $('.ks-cboxtags');
    $(".checkbox_container").css("max-height", ($(window).height() - list.offset().top) - 20);
    list.css({ 'min-height': list.parent().height(), 'max-height': list.parent().height() });
}

function load_data(data) {
    initialise_units_list(data);
    stretch_units_list();
    initialise_graph(data);
}

// Send a POST request
// axios({
//     method: 'POST',
//     url: 'http://10.42.0.50:5000/unit_category',
//     data: {
//         units_taken: ["C", "D"]
//     }
// })
//     .then(res => {
//         res.data = JSON.parse(res.data.replace(/'/g, '"'))
//         console.log(res.data);
//     })
//     .catch(err => {
//         console.log(err);
//     });

// var graph_data = JSON.parse("{\"nodes\":[{\"ID\":0,\"display\":\"AAAA1111\",\"colour\":\"white\"},{\"ID\":1,\"display\":\"BBBB1111\",\"colour\":\"white\"},{\"ID\":2,\"display\":\"CCCC1111\",\"colour\":\"white\"},{\"ID\":3,\"display\":\"DDDD1111\",\"colour\":\"white\"},{\"ID\":4,\"display\":\"EEEE1111\",\"colour\":\"white\"},{\"ID\":5,\"display\":\"FFFF1111\",\"colour\":\"white\"},{\"ID\":6,\"display\":\"GGGG1111\",\"colour\":\"white\"},{\"ID\":7,\"display\":\"HHHH1111\",\"colour\":\"white\"},{\"ID\":8,\"display\":\"or\",\"colour\":\"blue\"}],\"edges\":[{\"from\":3,\"to\":4,\"colour\":\"black\"},{\"from\":4,\"to\":5,\"colour\":\"white\"},{\"from\":8,\"to\":6,\"colour\":\"white\"},{\"from\":2,\"to\":7,\"colour\":\"white\"},{\"from\":1,\"to\":8,\"colour\":\"blue\"},{\"from\":2,\"to\":8,\"colour\":\"blue\"}]}");
// axios({
//     method: 'POST',
//     url: 'http://10.42.0.50:5000/get_all'
// })
//     .then(res => {
//         res.data = JSON.parse(res.data.replace(/'/g, '"'))
//         console.log(res.data);
//     graph_data = res.data;
//         load_data(graph_data);
// })
//     .catch(err => {
//         console.log(err);
//     });


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
    $("#graph_div").toggleClass("full_screen_graph");
    initialise_graph(graph_data);
}


function initialise_units_list(data) {
    if (!data) {
        return;
    }
    var str = "";

    var dataCopy = Object.assign({}, data);

    // Filter out "and" and "or" nodes.
    dataCopy.nodes = dataCopy.nodes.filter(x => x.display !== "and" && x.display !== "or");

    // Sort by the numbers in the unit code.
    dataCopy.nodes = dataCopy.nodes.sort((a, b) => {
        if (a.display < b.display)
            return -1;
        if (a.display > b.display)
            return 1;
        return 0;
    }); //a.display/*.slice(4)*/ - b.display/*.slice(4)*/)

    var lastUnitCodeCategory;
    var i = 0;
    for (var n of dataCopy.nodes) {
        if (lastUnitCodeCategory !== n.display.slice(0, 4) && lastUnitCodeCategory !== undefined) {
            str += `<hr>`;
        }

        str += `<li><input type="checkbox" id="checkbox${i}" value="${n.display}"><label
        for="checkbox${i}">${n.display}</label></li>`;
        i += 1;


        lastUnitCodeCategory = n.display.slice(0, 4);
        console.log(lastUnitCodeCategory)
    }

    $(".ks-cboxtags")[0].innerHTML = str;
}

var color_map = {
    "white": 'rgb(200, 200, 200)',
    "blue": 'rgb(0, 0, 255)',
    "red": 'rgb(255, 0, 0)',
    "black": 'rgb(0, 0, 0)'
}




function initialise_graph(data) {
    // console.log(data)
    var elementsToInput = [];

    var i = 0;
    for (var node of data.nodes) {
        elementsToInput.push({
            data: {
                id: i,
                display_name: node.display,
                color: color_map[node.colour]
            }
        });
        i++;
    }

    for (var edge of data.edges) {
        elementsToInput.push({
            data: {
                id: i,
                source: edge.from,
                target: edge.to,
                color: color_map[edge.colour]
            }
        });
        i++;
    }



    console.log(elementsToInput);

    $("#cy").innerHTML = "";
    var cy = cytoscape({
        container: $('#cy'),

        elements: elementsToInput,

        // elements: [ // list of graph elements to start with
        //     { // node a
        //         data: { id: 'a' }
        //     },
        //     { // node b
        //         data: { id: 'b' }
        //     },
        //     { // edge ab
        //         data: { id: 'ab', source: 'a', target: 'b' }
        //     }
        // ],

        style: [ // the stylesheet for the graph
            {

                //   {
                //     selector: ':parent',
                //     css: {
                //       'text-valign': 'top',
                //       'text-halign': 'center',
                //     }
                //   },

                selector: 'node',
                style: {
                    'background-color': 'data(color)',
                    'label': 'data(display_name)',
                    'content': 'data(display_name)',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'height': 50,
                    'width': 50
                }
            },

            {
                selector: 'edge',
                style: {
                    'width': 5,
                    'line-color': 'data(color)',
                    'target-arrow-color': 'data(color)',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier',
                    'opacity': 0.5
                }
            }
        ],

        layout: {
            name: 'dagre',
            rankDir: "TD",
            rankSep: 75,
            // directed: true,
            // // grid: true,
            // roots: ['#0'],
            // // rows: 1
        },

        // layout: {
        //     name: 'breadthfirst',
        //     directed: true,
        //     // // grid: true,
        //     // roots: ['#0'],
        //     // // rows: 1
        // },


        wheelSensitivity: 0.2,
        minZoom: 0.05,
        maxZoom: 3
    });
}