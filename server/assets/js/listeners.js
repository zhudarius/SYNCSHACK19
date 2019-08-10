function get_checked_boxes() {
    var checked_boxes = $('.ks-cboxtags :checkbox:checked');

    var checked_boxes_list = [];

    for (var key in checked_boxes) {
        if (checked_boxes.hasOwnProperty(key)) {
            // checked_boxes[key] = checked_boxes[key].value;
            checked_boxes_list.push(checked_boxes[key].value);
        }
    }

    // Get rid of any undefined
    checked_boxes_list = checked_boxes_list.filter(x => x !== undefined);
    return checked_boxes_list;
}

function units_can_do() {
    var checked_boxes_list = get_checked_boxes();

    console.log(checked_boxes_list);

    axios({
        method: 'POST',
        url: 'http://10.42.0.50:5000/unit_category',
        data: {
            units_taken: checked_boxes_list
        }
    })
        .then(res => {
            res.data = JSON.parse(res.data.replace(/'/g, '"'))

            Swal.fire({
                title: 'Data: ',
                text: res.data
            })
            console.log(res.data);

            // graph_data = res.data;
            // load_data(graph_data);
        })
        .catch(err => {
            // console.log(err);
            Swal.fire({
                title: err.toString(),
                type: 'error'
            })
        });

}


function how_to_take_unit() {
    var checked_boxes_list = get_checked_boxes();

    Swal.fire({
        title: 'What would you like to study?',
        input: 'text',
        inputAttributes: {
            'autocapitalize': 'on'
        },
        showCancelButton: true,
        confirmButtonText: 'Look up',
        showLoaderOnConfirm: true,
        preConfirm: (inputted) => {
            return axios({
                method: 'POST',
                url: 'http://10.42.0.50:5000/must_take',
                data: {
                    units_taken: checked_boxes_list,
                    target_unit: inputted
                }
            })
                .then(res => {
                    console.log(res.data);
                    return res.data
                })
                .catch(error => {
                    Swal.showValidationMessage(
                        `Request failed: ${error}`
                    )
                })
        },
        allowOutsideClick: () => !Swal.isLoading()
    }).then((result) => {
        console.log(result);

        Swal.fire({
            title: `Data:`,
            text: result.value
        })

    })


    // Swal.fire({
    //     title: 'What would you like to study?',
    //     input: 'text',
    //     showCancelButton: true,

    //     type: 'info',
    //     confirmButtonText: 'Ok'
    // });

}