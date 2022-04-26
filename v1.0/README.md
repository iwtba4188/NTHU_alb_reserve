# Reservation_of_NTHUalb

You can see full version in `readme` folder.

## Introduction
This is a tiny python script to auto reserve the court of the ALB in NTHU.

## Description

### Getting Start
Make sure you have installed `Python 3.7` or above.

And run these two commands in your command line.
```
$ pip install selenium
$ pip install webdriver_manager
```

### While Using
When you wants to start, just double-click `start.bat`.

Below is an example of `setting.json`.
``` json
./setting.json

{
    "id": "110999999",
    "password": "yourpassword",
    "place1": "1",
    "time1": "3",
    "place2": "1",
    "time2": "4",
    "target_date": "2022-05-20",
    "driver_type": "edge"
}
```

## Notice
- The court number is the row/col index (start from zero) in the table. For example, `"place1": "1", "time1": "3"` means that the `2nd` row and `4th` col in the table.
- You may enter the 5 days later today (you need this script only to reserve 5 days later). And the format is `YYYY-MM-DD`.

## Thanks
- Chrome extension [NTHU OAuth Decaptcha](https://github.com/justin0u0/NTHU-OAuth-Decaptcha) by [Justin0u0](https://github.com/justin0u0).

## Bugs
- Sometimes can't select second place correctly. But can still click by human and after alert raising, it can automatically click alert accept seccesfully.
