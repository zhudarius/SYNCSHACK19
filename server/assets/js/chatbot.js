var a;
$(".chatbot_input").on('keyup', function (e) {
    if (e.keyCode == 13) {
        // Do something
        console.log(e.currentTarget.value);
        console.log(get_checked_boxes());

        unit_code = e.currentTarget.value;


        addMessage(unit_code, "your_message");
        // $('.chat-box-ul')[0].animate({ scrollTop: $('.chat-box-ul').prop("scrollHeight") }, 500);



        // $('.chat-box-ul')[0].animate({
        //     scrollTop: $(".chat-box-ul li").last().offset().top
        // }, 'slow');

        axios({
            method: 'POST',
            url: `http://10.42.0.50:5000/compatible_unit/${unit_code}`,
            data: {
                units_taken: get_checked_boxes()
            }
        })
            .then(res => {
                // res.data = JSON.parse(res.data.replace(/'/g, '"'))
                console.log("returned data")
                console.log(res.data);

                addMessage(res.data, "their_message");
            })
            .catch(err => {
                console.log(err);
            });
    }
});


function addMessage(content, classType) {

    rawHTMLMsg = `<li class="chat_message ${classType}">
    ${content}
</li>`;

    $(".chat-box-ul")[0].innerHTML = $(".chat-box-ul")[0].innerHTML + rawHTMLMsg;


    var ul = $('.chat-box-ul')[0]
    ul.scrollTop = ul.scrollHeight

    // setTimeout(() => {
    //     $('.chat-box-ul')[0].animate({ scrollTop: $('.chat-box-ul')[0].scrollHeight }, 500);

    // }, 100);

}