<html>
<head>
    <meta charset="utf-8">
    <title>{{route_name}}</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

    <link rel="stylesheet" href="static/bootstrap.css" type="text/css">
    <link rel="stylesheet" href="static/style.css" type="text/css">
    <script src="https://code.jquery.com/jquery-3.4.1.min.js" type = "text/javascript"></script>
    <script src="static/bootstrap.js" type = "text/javascript"></script>
</head>
<body>
    <div class="container">
        <h1>Current route name is: {{route_name}} </h1>

        <div class="row"><div class="col-12">
            <table class="table table-dark table-hover table-responsible">
                % titles = list(map(lambda x: x[0], stops_list[0]))
                <thead><tr>
                    <th scope="col">#</th>
                    % for title in titles:
                        <th scope="col">{{title}}</th>
                    % end
                    <th scope="col">link</th>
                </tr></thead>
                <tbody>
                    % for i, stop in enumerate(stops_list):
                        <tr>
                            <th scope="row">{{i + 1}}</th>
                            % for col in stop:
                                <td>{{col[1]}}</td>
                            % end
                            <td><a href="/{{route_name}}/stop/{{stop.id}}" >Link</a></td>
                            %#<td><a href="https://www.google.com/">www</a></td>
                            %#<td><a href="">Blah Blah</a></td>
                        </tr>
                    % end
                </tbody>
            </table>
        </div></div>
    </div>
</body>
</html>