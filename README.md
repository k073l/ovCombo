# ovCombo

Automatically log into OpenVPN server using your combolist!

## Usage

`python main.py <args>`

`--openvpn-path` - Path to `openvpn.exe`, defaults to `ovpn/openvpn.exe`

`--config` - Path to `.ovpn` server config file, defaults to first `.ovpn` file found in `ovpn/`

`--outfile` - Filename to be used for combolist without dates or name of combolist in `output/` if you want to use already generated file

`--date` - `True` or `False`, set to True if your combolist has date set as follows: `mail:pass | YYYY-MM-DD HH:MM:SS`, defaults to `True`

`--timeout` - Timeout in seconds for OpenVPN client, defaults to `20`

Input combolist (if there's no file named as `outfile` in `output/`) will be grabbed from ovCombo's main directory.

Allowed combolist types:
`mail:pass`
`mail:pass | YYYY-MM-DD HH:MM:SS`

## Dependencies

Install [OpenVPN](https://openvpn.net/community-downloads/) and dump `OpenVPN/bin/` contents into `ovpn/` directory in ovCombo's main directory.
