import smb_inspector
import csv

host_server=''

def shares_searched(h):
    with open(f"{h}_shares.txt", "r") as s:
        reader = csv.reader(s)
        header = next(reader)  # Skip the header
        row_count = sum(1 for row in reader)
    return row_count

def interesting_found(h):
    with open(f"{h}_interesting.txt", "r") as s:
        reader = csv.reader(s)
        header = next(reader)  # Skip the header
        row_count = sum(1 for row in reader)
    return row_count

def dangerous_found(h):
    with open(f"{h}_dangers.txt", "r") as s:
        reader = csv.reader(s)
        header = next(reader)  # Skip the header
        row_count = sum(1 for row in reader)
    return row_count

def read_dangerous_found(h):
    result = ''
    with open(f"{h}_dangers.txt", "r") as s:
        lines = s.readlines()[1:]
        for line in lines:
            result +=f'''   <tr>
                            <td>{line.split(',')[0]}</td>
                            <td>{line.split(',')[1]}</td>
                            </tr>'''
    return result

def read_interesting_found(h):
    result = ''
    with open(f"{h}_interesting.txt", "r") as s:
        lines = s.readlines()[1:]
        for line in lines:
            result +=f'''   <tr>
                            <td>{line.split(',')[0]}</td>
                            <td>{line.split(',')[1]}</td>
                            </tr>'''
    return result

def read_interesting_found_chart(h):
    result = ''
    with open(f"{h}_interesting.txt", "r") as s:
        lines = s.readlines()[1:]
        for line in lines:
            result +=f'{line.split(',')[1]}'
    return result

def generate_report(host):
    global host_server
    host_server = host
    shares_count=shares_searched(host)
    interesting_count=interesting_found(host)
    dangerous_count=dangerous_found(host)
    read_danger=read_dangerous_found(host)
    read_interesting=read_interesting_found(host)
    chart_interesting_results=read_interesting_found_chart(host)

    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bug Bounty Output</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
    <link href="styles.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    </head>
    <nav class="navbar shadow navbar-expand-sm bg-dark navbar-dark">
    <div class="container-fluid">
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#collapsibleNavbar">
    <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="collapsibleNavbar">
    <ul class="navbar-nav">
    <li class="nav-item">
    <a class="nav-link">Dashboard</a>
    </li>
    </li>    
    </ul>
    </div>
    </div>
    </nav>
    <body class="background">
    <div class="container-fluid">
    <div class="row">
    <!-- Sidebar -->
    <div class="p-3 bordered-col shadow sidebar-bg text-center" id="sidebar-wrapper">
    <a class="text-center" href="#">
    <img src="https://github.com/Rainor23/smb_inspector/assets/45594693/76ca4544-6037-4bba-870d-30862ad8ec03" weidht="80" height="80" class="rounded-circle text-center" alt="">
    </a>
    <h4 class="">SMB Inspector Dashboard</h4>
    <hr>
    <ul class="nav nav-pills flex-column" id="hostList">
    <li class="nav-link"><i class='fas fa-eye Icon-colour m-2'></i><a href="#Overview">Overview</a></li>
    <li class="nav-link"><i class='fas fa-exclamation Icon-colour m-2'></i><a href="#dangerous">Dangerous</a></li>
    <li class="nav-link"><i class='fas fa-fingerprint Icon-colour m-2'></i><a href="#interesting">Interesting</a></li>
    </ul>
    </div>
    <!-- Main content -->
    <div class="col content-main">
    <div class="row">
    <div class="col p-2">
    <h1 class="display-4"></h1>
    <hr>
    </div>
    </div>
    <div class="row">
    <h2 class="fw-bold" id="Overview">Host Overview</h2>
    </div>
    <div class="row">
    <div class="col-12 col-sm-6 col-md-3">
    <div class="p-3 bordered-col bg-white shadow rounded hosts-bg">
    <div class="row">
    <div class="col ">
    <span class="summary-box">
        <i class='fas fas fa-user-secret icon m-2' style="font-size:36px;"></i>
    </span>
    </div>
    <div class="col fw-bold">
        Interesting files         
    </div>
    </div>
    <div class="row">
    <div class="text-center info-pad">
    '''

    html2='''
    </div>
    </div>
    </div>
    </div>
    <div class="col-12 col-sm-6 col-md-3">
    <div class="p-3 bordered-col bg-white shadow rounded hosts-bg">
    <div class="row">
    <div class="col ">
    <span class="summary-box">
    <i class='fas fa-exclamation-triangle icon m-2' style="font-size:36px;"></i>
    </span>
    </div>
    <div class="col fw-bold">
    Dangerous files         
    </div>
    </div>
    <div class="row">
    <div class="text-center info-pad">'''

    html3='''</div>
    </div>
    </div>
    </div>
    <div class="col-12 col-sm-6 col-md-3">
    <div class="p-3 bordered-col bg-white shadow rounded hosts-bg">
    <div class="row">
    <div class="col ">
    <span class="summary-box">
    <i class='fas fa-file-alt icon m-2' style="font-size:36px;"></i>
    </span>
    </div>
    <div class="col fw-bold">
    Total files         
    </div>
    </div>
    <div class="row">
    <div class="text-center info-pad">
    tba
    </div>
    </div>
    </div>
    </div>
    <div class="col-12 col-sm-6 col-md-3">
    <div class="p-3 bordered-col bg-white shadow rounded hosts-bg">
    <div class="row">
    <div class="col ">
    <span class="summary-box">
    <i class='fas fa-laptop-house icon m-2' style="font-size:36px;"></i>
    </span>
    </div>
    <div class="col fw-bold">
    Shares scanned         
    </div>
    </div>
    <div class="row">
    <div class="text-center info-pad">'''

    html4='''</div>
    </div>
    </div>
    </div>
    </div>
    <div class="row">
    <div class="col p-3 bordered-col bg-white shadow rounded files-bg m-2">
    <div class="card">
    <div class="card-header">
    <h5 class="card-title">Dangerous Files</h5>
    </div>
    <div class="card-body">
    <div class="row">
    <div class="col-md-8 results-bg">
    <p class="text-center">
    <strong>Found Dangerous Files</strong>
    </p>
    <table class="table table-striped">
    <thead>
    <tr>
    <th scope="col">Host</th>
    <th scope="col">File</th>
    <th scope="col">Permission</th>
    </tr>
    </thead>
    <pre>
    
    '''

    html5='''
    </pre>
    </table>
    </div>
    </div>
    </div>
    </div>
    </div>
    </div>
    <div class="row">
    <div class="col p-3 bordered-col bg-white shadow rounded files-bg m-2">
    <div class="card">
    <div class="card-header">
    <h5 class="card-title">Interesting Files</h5>
    </div>
    <div class="card-body">
    <div class="row">
    <div class="col-md-8 results-bg">
    <p class="text-center">
    <strong>Found Interesting Files</strong>
    </p>
    <table class="table table-striped">
    <thead>
    <tr>
    <th scope="col">Host</th>
    <th scope="col">File</th>
    </tr>
    </thead>
    <pre>
    '''

    html6='''
    </pre>
    </table>
    </div>
    <div class="col-md-4">
        <p class="text-center">
            <strong>Found File Extensions</strong>
        </p>
        <canvas id="myChart"></canvas>
    </div>
    <script src="chart-data.js"></script>
    </div>
    </div>
    </div>
    </div>
    </div>
    </div>
    </div>
    </div>
    </div>
    <script>
    function selectHost(element) {
    // Remove 'active' class from all links
    document.querySelectorAll('.nav-link').forEach(link => {
    link.classList.remove('active');
    });

    // Add 'active' class to the clicked link
    element.classList.add('active');
    }
    </script>
    <script>
    $(document).ready(function() {
    $("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#sidebar-wrapper").toggleClass("toggled");
    });
    });
    </script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="scripts.js"></script>
    </body>
    </html>
    '''

    report = html + str(interesting_count) + html2 + str(dangerous_count) + html3 + str(shares_count) + html4 + read_danger + html5 + read_interesting + html6

    css='''
    :root {
        --font-family-sans-serif: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }

    body {
        overflow-x: hidden;
        overflow-y: scroll;
        font-family: var(--font-family-sans-serif);
    }

    /* Custom styles */
    .background {
        background-color: #e6e6e6;
    }
    .nav-colour {
        background-color: #6F7871;
    }
    .Icon-colour {
        color: #F0F1EE;
    }
    .nav-pills {
        color: #F0F1EE;
    }

    #hostList a {
        cursor: pointer;
    }
    .pre {
        position: relative; /* Ensures the <pre> tag is positioned relative to .scrollable-pre */
        overflow-y: auto;   /* Enable scrolling within the <pre> itself */
    }
    .bordered-col {
        padding: 10px;
        margin-bottom: 20px; /* Space between sections */
    }
    .boarder {
        border: 2px solid #1d3557; /* Bootstrap's border color for consistency */
    }
    .hosts-bg, .results-bg {
        max-height: 600px; /* Maximum height before scrolling */
        overflow-y: auto; /* Allows scrolling within the sidebar if content is too long */
    }
    .files-bg{
        max-height: 650px; /* Maximum height before scrolling */
        overflow-y: hidden;
    }
    .prescroll {
        overflow-y: auto;   /* Enables vertical scrolling within the <pre> */
        position: relative; /* Ensures positioning is relative to the .hosts-bg container */
    }
    .sidebar-bg a {
        color: #F0F1EE !important; /* Ensures all links are white */
        text-decoration: none !important; /* Removes underline from links */
    }
    .sidebar-bg a:hover {
        padding-left: 20px; /* Slight indentation on hover */
        transition: all 0.3s ease-in-out; /* Smooth transition for hover effects */
        text-decoration: none !important; /* Removes underline from links */
    }
    .nav-link {
        padding: 10px 15px; /* More padding for each link */
        font-size: 16px; /* Larger font size for better readability */
        
    }
    .sidebar-heading {
        padding: 15px 15px 10px; /* Adjust padding for the heading */
        border-bottom: 1px solid #475569; /* Adds a subtle border under the heading for separation */
        margin-bottom: 10px; /* Spacing after the heading */
    }
    .sidebar-bg {
        background-color: #2C3432; /* A dark, soothing background color */
        min-height: 100vh; /* Ensures the sidebar extends to the full height of the viewport */
        position: fixed; /* Position fixed relative to the viewport */
        width: 200px;
        top: 0;
        color: #F0F1EE;
    }
    .active {
        background-color: #dee2e6; /* A distinct background color for active link */
        color: #ffffff; /* White text color for better contrast */
        padding-left: 30px; /* Increased padding for emphasis */
        border-radius: 5px; /* Optional: rounded corners for aesthetic */
        transition: padding 0.3s ease; /* Smooth transition for padding changes */
        text-decoration: none !important; /* Removes underline from links */
    }
    .fit-image {
        object-fit: cover;
    }
    .content-main {
        margin-left: 200px;
    }
    .navbar {
        margin-left: 200px;
        
    }
    .fa-exclamation-triangle {
        color: red;
    }
    .info-pad {
        padding-top: 5px;
        font-size:x-large;
    }
    .DivWithScroll{
    overflow:scroll;
    overflow-x:hidden;
    }
    .Divheight{
    height: 300px;
    }
    '''

    chart_interesting='''
    // Define the data
    const data = `
    '''+ chart_interesting_results +'''
    `;

    // Parse the data and count the file extensions
    const lines = data.trim().split('\\n');
    const extensionCounts = {};

    lines.forEach(line => {
        const parts = line.split('/');
        const fileName = parts[parts.length - 1];
        const extension = fileName.split('.').pop();
        if (extensionCounts[extension]) {
            extensionCounts[extension]++;
        } else {
            extensionCounts[extension] = 1;
        }
    });

    // Prepare data for Chart.js
    const labels = Object.keys(extensionCounts);
    const counts = Object.values(extensionCounts);

    // Define background colors
    const backgroundColors = [
        'rgba(75, 192, 192, 0.2)',
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(199, 199, 199, 0.2)',
        'rgba(83, 102, 255, 0.2)',
        'rgba(255, 100, 64, 0.2)',
        'rgba(75, 200, 192, 0.2)',
        'rgba(255, 90, 86, 0.2)',
    ];

    // Extend or reduce backgroundColors array to match the number of labels
    const bgColors = backgroundColors.slice(0, labels.length);

    // Ensure we have enough colors for all labels
    while (bgColors.length < labels.length) {
        bgColors.push(...backgroundColors);
        bgColors.length = labels.length;
    }

    document.addEventListener("DOMContentLoaded", function() {
        // Create the Chart.js chart
        const ctx = document.getElementById('myChart').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'File Extension Count',
                    data: counts,
                    backgroundColor: bgColors,
                    borderColor: bgColors.map(color => color.replace('0.2', '1')),
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    });
    '''


    with open("styles.css", "w+") as r:
        r.write(css)
    with open("chart-data.js", "w+") as r:
        r.write(chart_interesting)
    with open("report.html", "w+") as r:
        r.write(report)
