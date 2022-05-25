function submit_form(){
    document.getElementsByClassName("poll-form").submit();
}

function delete_option(source_class){
    var question_no = source_class.split(' ')[0];
    var current_options = document.getElementsByClassName(question_no)[0].getElementsByClassName(question_no+" O");
    var current_delete_buttons = document.getElementsByClassName(question_no)[0].getElementsByClassName(question_no+" B");
    var current_line_breaks = document.getElementsByClassName(question_no)[0].getElementsByTagName('br');
    var question = document.getElementsByClassName(question_no)[0];
    var current_input_values = [];
    var current_options_len = current_options.length;

    if (current_options_len > 2){
        for (var i=(current_options_len-1); i>-1; i--){ 
            if (current_options[i].className != source_class.replace("B", "O")){
                current_input_values.push(current_options[i].value);
            }
            question.removeChild(current_options[i]);
            question.removeChild(current_delete_buttons[i]);
            question.removeChild(current_line_breaks[i]);
        }
        var add_option_button = document.getElementsByClassName(question_no+' B add-option')[0];
        for (i=0; i<current_input_values.length; i++){
            var input_element = document.createElement("INPUT");
            input_element.setAttribute("type", 'text');
            input_element.setAttribute("name", question_no+'O'+(i+1));
            input_element.setAttribute("class", question_no+' O '+(i+1))
            input_element.setAttribute("placeholder", "Option "+(i+1));
            input_element.setAttribute("value", current_input_values[i]);
            input_element.setAttribute("required", true);
            question.insertBefore(input_element, add_option_button);
            var delete_element = document.createElement("BUTTON");
            delete_element.setAttribute("class", question_no+' B '+(i+1));
            delete_element.setAttribute("type", 'button');
            delete_element.setAttribute("onclick", "delete_option(this.className)");
            delete_element.innerText = "remove";
            question.insertBefore(delete_element, add_option_button);
            question.insertBefore(document.createElement("BR"), add_option_button);
        }
    }
    else{
        alert("At least 2 options are necessary");
    }
}

function add_option(source_class){
    var question_no = source_class.split(' ')[0];
    var current_options = document.getElementsByClassName(question_no)[0].getElementsByClassName(question_no+" O");
    var question = document.getElementsByClassName(question_no)[0];
    var current_options_len = current_options.length;
    
    if (current_options_len < 10){
        var add_option_button = document.getElementsByClassName(question_no+' B add-option')[0];
        var input_element = document.createElement("INPUT");
        input_element.setAttribute("type", 'text');
        input_element.setAttribute("name", question_no+'O'+(current_options_len+1));
        input_element.setAttribute("class", question_no+' O '+(current_options_len+1))
        input_element.setAttribute("placeholder", "Option "+(current_options_len+1));
        input_element.setAttribute("value", "");
        input_element.setAttribute("required", true);
        question.insertBefore(input_element, add_option_button);
        var delete_element = document.createElement("BUTTON");
        delete_element.setAttribute("class", question_no+' B '+(current_options_len+1));
        delete_element.setAttribute("type", 'button');
        delete_element.setAttribute("onclick", "delete_option(this.className)");
        delete_element.innerText = "remove";
        question.insertBefore(delete_element, add_option_button);
        question.insertBefore(document.createElement("BR"), add_option_button);
    }
    else{
        alert("Max 10 options can be added");
    }
}

function add_question(){
    var question_box = document.getElementsByClassName("poll-questions-box")[0];
    var add_question_button = document.getElementsByClassName("add-question")[0];
    var question = document.createElement("DIV");
    
    if (question_box.getElementsByTagName('div').length < 20){
        var current_question_len = question_box.getElementsByTagName("div")[(question_box.getElementsByTagName("div").length)-2].className.replace("Q", "");
        current_question_len = parseInt(current_question_len) + 1;
        question.setAttribute("class", "Q"+current_question_len);
        question_box.insertBefore(question, add_question_button);

        var question_label_div = document.createElement("DIV");
        var question_label = document.createElement("LABEL")
        question_label.innerText = "Question: ";
        var question_input = document.createElement("INPUT");
        question_input.setAttribute("type", "text");
        question_input.setAttribute("name", "Q"+current_question_len);
        question_input.setAttribute("placeholder", "Enter a question");
        question_input.setAttribute("value", "");
        question_input.setAttribute("required", true);
        var question_delete_button = document.createElement("BUTTON");
        question_delete_button.setAttribute("class", "Q"+current_question_len);
        question_delete_button.setAttribute("type", 'button');
        question_delete_button.setAttribute("onclick", "delete_question(this.className)");
        question_delete_button.innerText = "remove";
        question_label_div.appendChild(question_label);
        question_label_div.appendChild(document.createElement("BR"));
        question_label_div.appendChild(question_input);
        question_label_div.appendChild(question_delete_button);
        question.appendChild(question_label_div);

        for (var i=1; i<3; i++){
            var option_input = document.createElement("INPUT");
            option_input.setAttribute("type", "text");
            option_input.setAttribute("class", "Q"+current_question_len+" O "+i);
            option_input.setAttribute("placeholder", "Option "+i);
            option_input.setAttribute("name", "Q"+current_question_len+"O"+i);
            option_input.setAttribute("value", "");
            option_input.setAttribute("required", true);
            var option_delete_button = document.createElement("BUTTON");
            option_delete_button.setAttribute("class", "Q"+current_question_len+" B "+i);
            option_delete_button.setAttribute("type", 'button');
            option_delete_button.setAttribute("onclick", "delete_option(this.className)");
            option_delete_button.innerText = "remove";
            question.appendChild(option_input);
            question.appendChild(option_delete_button);
            question.appendChild(document.createElement("BR"));
        }

        var add_option_button = document.createElement("BUTTON");
        add_option_button.setAttribute("class", "Q"+current_question_len+" B add-option");
        add_option_button.setAttribute("type", 'button');
        add_option_button.setAttribute("onclick", "add_option(this.className)");
        add_option_button.innerText = "add option";
        question.appendChild(add_option_button);
        question.appendChild(document.createElement("HR"));
    }
    else{
        alert("Max 10 questions can be added")
    }
}

function delete_question(source_class){
    var question_box = document.getElementsByClassName("poll-questions-box")[0];
    if (question_box.getElementsByTagName('div').length > 2){
        question_box.removeChild(question_box.getElementsByClassName(source_class)[0]);
    }
    else{
        alert("At least 1 question is necessary");
    }
}