(function ($) {
    $(document).ready(function () {
        var $redOrBlue = $("#red_or_blue");
        if ($redOrBlue.length) {
            $.getJSON("/games/stats/?statistic=red_or_blue", function (data) {
                var chart = new Chart($redOrBlue, data);
            });
        }
        var $players = $("#players-stats");
        if ($players.length) {
            $.getJSON("/games/stats/?statistic=players", function (data) {
                var chart = new Chart($players, data);
            });
        }
    });
}(jQuery));
