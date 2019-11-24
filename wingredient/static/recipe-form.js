$(document).ready(function(){
    var next = 1;
    $(".add-more").click(function(e){
        console.log("test bitch")
        e.preventDefault();
        var addto = "#field" + next;
        var addRemove = "#field" + (next);
        next = next + 1;
        var newIn = '<textarea autocomplete="off" style="float: left; width: 92%;" class="input form-control" id="field' + next + '" name="field' + next + '" type="text"></textarea>';
        var newInput = $(newIn);
        var removeBtn = '<button id="remove' + (next - 1) + '" class="btn btn-danger remove-me" style="float: left; margin:2px;">-</button></div><div id="field" style="width: 100%;">';
        var removeButton = $(removeBtn);
        document.getElementById("count").val = next;
        console.log(newIn)
        $(addto).after(newInput);
        $(addRemove).after(removeButton);
        $("#field" + next).attr('data-source',$(addto).attr('data-source'));
        $("#count").val(next);  
        
            $('.remove-me').click(function(e){
                e.preventDefault();
                var fieldNum = this.id.charAt(this.id.length-1);
                var fieldID = "#field" + fieldNum;
                $(this).remove();
                $(fieldID).remove();
            });
    });

    var ingredient_next = 1;
    $(".add-more-ingredient").click(function(e){
        console.log("add more ingredine")
        console.log(all_ingredients)
        e.preventDefault();
        var addto = "#field-ingredient" + ingredient_next;
        var addRemove = "#field-ingredient" + (ingredient_next);
        ingredient_next = ingredient_next + 1;
        var optionsAsString = "";
        for(var i = 0; i < all_ingredients.length; i++) {
            optionsAsString += "<option value='" + all_ingredients[i] + "'>" + all_ingredients[i] + "(" + m_types[i] + ")" + "</option>";
        }
        var newIn = '<div id="field-ingredient' + ingredient_next + '" name="field-ingredient' + ingredient_next + '"><select name="ingredient' + ingredient_next +'" id="ingredients" class="form-control" style="float: left; width: 50%;">' + optionsAsString + '</select><input type="number" style="height: 38px; width: 30%; float: left;" class="form-control input-lg" min="0" step="1" name="ingredient-quantity' + ingredient_next + '" id="quantity" placeholder="Quantity" required/><input class="form-control form-check-inline" style="width: 2%; margin-left: 20px; float:left;" type="checkbox" name="ingredient_check' + ingredient_next +'" id="ingredient_check"/></div>';
        var newInput = $(newIn);
        var removeBtn = '<button id="remove-ingredient' + (ingredient_next - 1) + '" class="btn btn-danger remove-me-ingredient" style="float: left; margin:2px;">-</button></div><div id="field-ingredient" style="width: 100%;">';
        var removeButton = $(removeBtn);
        document.getElementById("count-ingredient").val = ingredient_next;
        $(addto).after(newInput);
        $(addRemove).after(removeButton);
        console.log(addto)
        $("#field-ingredient" + ingredient_next).attr('data-source',$(addto).attr('data-source'));
        $("#count-ingredient").val(ingredient_next);  
        
            $('.remove-me-ingredient').click(function(e){
                e.preventDefault();
                var fieldNum = this.id.charAt(this.id.length-1);
                var fieldID = "#field-ingredient" + fieldNum;
                $(this).remove();
                $(fieldID).remove();
            });
    });

});



//<div id="field-ingredient' + ingredient_next + '" name="field-ingredient' + ingredient_next + '"><select name="ingredients" id="ingredients" class="form-control" style="float: left; width: 50%;"> % for i in range(len(all_ingredients)):<option value="${all_ingredients[i]}">${all_ingredients[i]} (${m_types[i]})</option>% endfor</select><input type="number" style="height: 38px; width: 40%; float: left;" class="form-control input-lg" min="0" step="1" name="quantity" id="quantity" placeholder="Quantity" required/></div>