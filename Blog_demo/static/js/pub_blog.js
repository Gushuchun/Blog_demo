window.onload = function () {
    const { createEditor, createToolbar } = window.wangEditor;

    const editorConfig = {
        placeholder: 'Type here...',
        onChange(editor) {
            const html = editor.getHtml();
            console.log('editor content', html);
            // 也可以同步到 <textarea>
        }
    };

    const editor = createEditor({
        selector: '#editor-container',
        html: '<p><br></p>',
        config: editorConfig,
        mode: 'default', // or 'simple'
    });

    const toolbarConfig = {};

    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container',
        config: toolbarConfig,
        mode: 'default', // or 'simple'
    });

    $("#submit-btn").click(function(event) {
        // Prevent default button behavior
        event.preventDefault();

        // Clear previous error messages
        $(".error-message").remove();

        // Get form values
        let title = $("input[name='title']").val().trim();
        let category = $("#category-select").val();
        let content = editor.getHtml()
        let content_2 = editor.getText().trim()
        let csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();

        // Validation flags
        let valid = true;

        // Title validation
        if (!title) {
            $("label[for='title']").append('<span class="error-message" style="color: red; margin-left: 10px;">Can not be None</span>');
            valid = false;
        }

        // Content validation
        if (!content_2) {  // Checks for empty HTML in content
            $("label[for='content']").append('<span class="error-message" style="color: red; margin-left: 10px;">Can not be None</span>');
            valid = false;
        }

        // If validation fails, stop submission
        if (!valid) {
            return;
        }

        // AJAX request if all fields are valid
        $.ajax('/blog/post', {
            method: 'POST',
            data: { title, category, content, content_2, csrfmiddlewaretoken },
            success: function (result) {
                if (result['code'] == 200) {
                    let blog_id = result['data']['blog_id'];
                    window.location = '/blog/detail/' + blog_id;
                } else {
                    alert(result['message']);
                }
            }
        });
    });
}
