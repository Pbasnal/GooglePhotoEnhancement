$(function() {
    $('#name').keyup(function() {
        $("#greet").text("Greet gata chal! Oh " + $("#name").val() + " gungunata chal!");
    })
})