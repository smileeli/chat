function Infer() {
}

Infer.prototype.changeInput = function () {
    // var parameter = $("#parameters_select").find("option:selected").val();
    $("#parameters_select").change(function (){
        var parameter = $("#parameters_select").find("option:selected").val();
        if(parameter=='测试集'){
            $(".input-args2").css('display','inline');
            $(".send-config").css('display','none');
            $(".input-args").css('display','none');
    } else{
            $(".input-args").css('display','inline');
            $(".send-config").css('display','inline');
            $(".input-args2").css('display','none');
    };
    })
}

Infer.prototype.addArgs = function () {
    var submitBtn = $('.submit-config-btn');
    var content = $('#input-content').val();
    console.log('111')
    // $('#parameters-choice').change(function () {
    //     window.parameter = $("#parameters-choice").find("option:selected").val()
    // });
    // console.log(parameter)
    submitBtn.click(function () {
            var content = $('#input-content').val();
            var parameter = $("#parameters_select").find("option:selected").val();
            console.log(content, parameter);
            if (parameter != '测试集') {
                aichatajax.post({
                    'url': '/infer/add_args/',
                    'data': {
                        'parameter': parameter,
                        'content': content,
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            var content = result['data'];
                            alert(content);
                        }
                    }
                });
            }else{
                alert('正在上传');
            }

        }
    )
}

Infer.prototype.addInfers = function () {
    var submitBtn2 = $('.submit-args-btn');
    submitBtn2.click(function (){
        var model = $("#model_select").find("option:selected").val();
        var text = $("#text_select").find("option:selected").val();
        var type = $("#type_select").find("option:selected").val();
        var prompt_ = $("#prompt_select").find("option:selected").val();
        var thread = $("#thread_select").find("option:selected").val();
        console.log(model,text,type,prompt_,thread);
        aichatajax.post({
            'url': 'infer/add_infers/',
            'data':{
                'name': model,
                'file': text,
                'type': type,
                'prompt': prompt_,
                'thread': thread,
                'status': '0',
            },
            'success': function (result) {
                if(result['code'] === 200){
                    var comment = result['data'];
                    if(comment=='请勿重复提交任务'){
                        alert(comment)
                    }else{
                        location.reload();
                    }
                }
            }
        });
        }

    )

}

Infer.prototype.deleteInfers = function () {
    var deleteBtn = $('.delete-btn');
    deleteBtn.click(function (){
        var btn=$(this);
        var infer_id=btn.attr('infer-id')
        aichatajax.post({
            'url': 'infer/delete_infers/',
            'data':{
                'infer_id': infer_id,
            },
            'success': function (result) {
                if(result['code'] === 200){
                    var comment = result['data'];
                    alert(comment);
                    location.reload();
                }
            }
        });
        }

    )

}

Infer.prototype.begainInfers = function () {
    var begainBtn = $('.begain-btn');
    begainBtn.click(function (){
        var btn=$(this);
        var infer_id=btn.attr('infer-id');
        // $('#infers  td').each(function (){
        //     if($(this).text()==infer_id){
        //         window.row=$(this).closest('tr').prevAll().length+1;
        //     }
        //     }
        // )
        // $('#infers').find("tr").eq(row).find("td").eq(5).text('已开始');
        aichatajax.post({
            'url': 'infer/begain_infers/',
            'data':{
                'infer_id': infer_id,
            },
            // 'success': function (result) {
            //     if(result['code'] === 200){
            //         alert('已开始');
            //     }
            // }
        });
        }
    )
}

// Infer.prototype.download = function () {
//     var downloadBtn = $('.download-btn');
//     downloadBtn.click(function (){
//         var btn=$(this);
//         var infer_id=btn.attr('infer-id');
//         aichatajax.post({
//             'url': 'infer/download/',
//             'data':{
//                 'infer_id': infer_id,
//             },
//             'success': function (result) {
//                 if(result['code'] === 200){
//                     var disp = request.getResponseHeader('Content-Disposition');
//                     var form = $('<form action="/infer/download/" method="post"></form>');
//                     $('body').append(form);
//                     form.submit();
//                 }
//             }
//         });
//         }
//     )
// }


Infer.prototype.run = function () {
    this.addArgs();
    this.changeInput();
    this.addInfers();
    this.deleteInfers();
    this.begainInfers();
    // this.download();
    // this.changeStatus();
};


$(function () {
    var infer = new Infer();
    infer.run();
});

