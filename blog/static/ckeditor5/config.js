$(document).ready(function () {
    ClassicEditor
        .create( document.querySelector('#id_content'), {
            toolbar: {
                items: [
                        'heading',
                        '|',
                        'fontColor',
                        'fontFamily',
                        'fontSize',
                        'fontBackgroundColor',
                        'bold',
                        'link',
                        'italic',
                        'bulletedList',
                        'numberedList',
                        'highlight',
                        '|',
                        'outdent',
                        'indent',
                        '|',
                        'imageUpload',
                        'insertTable',
                        'mediaEmbed',
                        'blockQuote',
                        'codeBlock',
                        'code',
                        'sourceEditing',
                        'CKFinder',
                ]
            },
            language: 'zh-cn',
            image: {
                toolbar: [
                    'imageTextAlternative',
                    'imageStyle:inline',
                    'imageStyle:block',
                    'imageStyle:side',
                    'linkImage'

                ]
            },
            //上传图片url配置
            ckfinder: {
                uploadUrl: '/uploads/'
            },
            table: {
                contentToolbar: [
                    'tableColumn',
                    'tableRow',
                ]
            },
            licenseKey: '',

            } )

            .then( editor => {
                window.editor = editor;

            } )
            .catch( error => {
                console.error( 'Oops, something went wrong!' );
                console.error( 'Please, report the following error on https://github.com/ckeditor/ckeditor5/issues with the build id and the error stack trace:' );
                console.warn( 'Build id: t0fabmaqb2nt-4idr9zq80ggc' );
                console.error( error );
            } );

})