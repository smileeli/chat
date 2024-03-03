function Aichat() {
}

Aichat.prototype.changeModel = function () {
    var model_title = $('#model_title');
    $('#model_select').change(function (){
        var checkText = $("#model_select").find("option:selected").text();
        model_title.text(checkText)
        }
    )
}

Aichat.prototype.changePrompt = function () {
    var prompt_textarea = $("textarea[name='prompt-text']");
    $('#prompt_select').change(function (){
        var checkText = $("#prompt_select").find("option:selected").text();
        prompt_textarea.val(checkText)
        }
    )
}

Aichat.prototype.sendPrompt = function () {
    var submitBtn = $('.submit-btn');
    var query_textarea = $("textarea[name='query']");
    var prompt_textarea = $("textarea[name='prompt-text']");
    var model_title = $('#model_title');
    submitBtn.click(function (){
        var query= query_textarea.val();
        var prompt= prompt_textarea.val();
        var model=model_title.text();
        console.log(model+prompt+query);
        aichatajax.post({
            'url': 'response/',
            'data':{
                'model': model,
                'prompt': prompt,
                'query':query
            },
            'success': function (result) {
                if(result['code'] === 200){
                    var comment = result['data'];
                    var aa=$('.response-content');
                    console.log(1);
                    console.log(aa.text());
                    aa.text(comment);
                    console.log(comment);
                }
            }
        });
        }
    )
}

Aichat.prototype.run = function () {
    this.changeModel();
    this.changePrompt();
    this.sendPrompt();
};


$(function () {
    var aichat = new Aichat();
    aichat.run();
});

