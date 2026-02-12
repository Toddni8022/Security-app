Add-Type -AssemblyName System.Windows.Forms

# Create a form
$form = New-Object System.Windows.Forms.Form
$form.Text = 'Dancing Robot'
$form.WindowState = 'Maximized'
$form.FormBorderStyle = 'None'
$form.BackColor = [System.Drawing.Color]::White

# Create a label for the dancing robot
$label = New-Object System.Windows.Forms.Label
$label.Font = New-Object System.Drawing.Font('Arial', 100)
$label.AutoSize = $true
$label.Text = '🤖'
$form.Controls.Add($label)

# Set the initial position
$left = ([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width / 2) - ($label.Width / 2)
$top = ([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height / 2) - ($label.Height / 2)
$label.Location = New-Object System.Drawing.Point($left, $top)

# Random dance moves
$timer = New-Object System.Windows.Forms.Timer
$timer.Interval = 200
$timer.Add_Tick({
    $left += (Get-Random -Minimum -20 -Maximum 20)
    $top += (Get-Random -Minimum -20 -Maximum 20)
    $label.Location = New-Object System.Drawing.Point($left, $top)
})
$timer.Start()
$form.Add_Shown({$form.Activate()})
[void]$form.ShowDialog()