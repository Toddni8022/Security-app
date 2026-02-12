Add-Type -AssemblyName System.Windows.Forms

# Create a form
$form = New-Object System.Windows.Forms.Form
$form.Text = 'Bouncing Text'
$form.WindowState = 'Maximized'
$form.FormBorderStyle = 'None'
$form.BackColor = [System.Drawing.Color]::Black
$label = New-Object System.Windows.Forms.Label
$label.ForeColor = [System.Drawing.Color]::White
$label.Font = New-Object System.Drawing.Font('Arial', 50)
$label.AutoSize = $true
$label.Text = 'HAL is cool!'
$form.Controls.Add($label)

# Set the position
$left = Get-Random -Minimum 0 -Maximum ([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width - $label.Width)
$top = Get-Random -Minimum 0 -Maximum ([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height - $label.Height)
$label.Location = New-Object System.Drawing.Point($left, $top)

# Animation loop
$timer = New-Object System.Windows.Forms.Timer
$timer.Interval = 100
$timer.Add_Tick({
    $left += 10
    if ($left -gt ([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width)) {
        $left = -$label.Width
    }
    $label.Location = New-Object System.Drawing.Point($left, $top)
})
$timer.Start()
$form.Add_Shown({$form.Activate()})
[void]$form.ShowDialog()