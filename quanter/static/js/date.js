/**
 * Created by StevenWu on 17/1/2.
 */
var picker = new Pikaday(
    {
        field: document.getElementById('start'),
        firstDay: 1,
        minDate: new Date('2010-01-01'),
        maxDate: new Date('2020-12-31'),
        yearRange: [2010,2020],
        onSelect: function() {
            var date = document.createTextNode(this.getMoment().format('Do MMMM YYYY') + ' ');
        }
    });
picker.setMoment(moment());

var picker1 = new Pikaday(
    {
        field: document.getElementById('end'),
        firstDay: 1,
        minDate: new Date('2010-01-01'),
        maxDate: new Date('2020-12-31'),
        yearRange: [2010,2020],
        onSelect: function() {
            var date = document.createTextNode(this.getMoment().format('Do MMMM YYYY') + ' ');
        }
    });
picker1.setMoment(moment());

var picker2 = new Pikaday(
    {
        field: document.getElementById('loop_start'),
        firstDay: 1,
        minDate: new Date('2010-01-01'),
        maxDate: new Date('2020-12-31'),
        yearRange: [2010,2020],
        onSelect: function() {
            var date = document.createTextNode(this.getMoment().format('Do MMMM YYYY') + ' ');
        }
    });
picker2.setMoment(moment());

var picker3 = new Pikaday(
    {
        field: document.getElementById('loop_end'),
        firstDay: 1,
        minDate: new Date('2010-01-01'),
        maxDate: new Date('2020-12-31'),
        yearRange: [2010,2020],
        onSelect: function() {
            var date = document.createTextNode(this.getMoment().format('Do MMMM YYYY') + ' ');
        }
    });
picker3.setMoment(moment());