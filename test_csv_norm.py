import io
import pytest
from csv_norm import csv_norm


GOOD_CSV_INPUT = """\
Timestamp,Address,ZIP,FullName,FooDuration,BarDuration,TotalDuration,Notes
4/1/11 11:00:00 AM,"123 4th St, Anywhere, AA",94121,Monkey Alberto,1:23:32.123,1:32:33.123,zzsasdfa,I am the very model of a modern major general
3/12/14 12:00:00 AM,"Somewhere Else, In Another Time, BB",1,Superman übertan,111:23:32.123,1:32:33.123,zzsasdfa,This is some Unicode right here. ü ¡! 😀
2/29/16 12:11:11 PM,111 Ste. #123123123,1101,Résumé Ron,31:23:32.123,1:32:33.123,zzsasdfa,🏳️🏴🏳️🏴
1/1/11 12:00:01 AM,"This Is Not An Address, BusyTown, BT",94121,Mary 1,1:23:32.123,0:00:00.000,zzsasdfa,I like Emoji! 🍏🍎😍
12/31/16 11:59:59 PM,"123 Gangnam Style Lives Here, Gangnam Town",31403,Anticipation of Unicode Failure,1:23:32.123,1:32:33.123,zzsasdfa,I like Math Symbols! ≱≰⨌⊚
11/11/11 11:11:11 AM,überTown,10001,Prompt Negotiator,1:23:32.123,1:32:33.123,zzsasdfa,"I’m just gonna say, this is AMAZING. WHAT NEGOTIATIONS."
5/12/10 4:48:12 PM,Høøük¡,1231,Sleeper Service,1:23:32.123,1:32:33.123,zzsasdfa,2/1/22
10/5/12 10:31:11 PM,"Test Pattern Town, Test Pattern, TP",121,株式会社スタジオジブリ,1:23:32.123,1:32:33.123,zzsasdfa,1:11:11.123
10/2/04 8:44:11 AM,The Moon,11,HERE WE GO,1:23:32.123,1:32:33.123,zzsasdfa,
"""

GOOD_CSV_NORMALIZED = """\
Timestamp,Address,ZIP,FullName,FooDuration,BarDuration,TotalDuration,Notes
2011-04-01T14:00:00-04:00,"123 4th St, Anywhere, AA",94121,MONKEY ALBERTO,5012.123,5553.123,10565.246,I am the very model of a modern major general
2014-03-12T03:00:00-04:00,"Somewhere Else, In Another Time, BB",00001,SUPERMAN ÜBERTAN,401012.123,5553.123,406565.24600000004,This is some Unicode right here. ü ¡! 😀
2016-02-29T15:11:11-05:00,111 Ste. #123123123,01101,RÉSUMÉ RON,113012.123,5553.123,118565.24600000001,🏳️🏴🏳️🏴
2011-01-01T03:00:01-05:00,"This Is Not An Address, BusyTown, BT",94121,MARY 1,5012.123,0.0,5012.123,I like Emoji! 🍏🍎😍
2017-01-01T02:59:59-05:00,"123 Gangnam Style Lives Here, Gangnam Town",31403,ANTICIPATION OF UNICODE FAILURE,5012.123,5553.123,10565.246,I like Math Symbols! ≱≰⨌⊚
2011-11-11T14:11:11-05:00,überTown,10001,PROMPT NEGOTIATOR,5012.123,5553.123,10565.246,"I’m just gonna say, this is AMAZING. WHAT NEGOTIATIONS."
2010-05-12T19:48:12-04:00,Høøük¡,01231,SLEEPER SERVICE,5012.123,5553.123,10565.246,2/1/22
2012-10-06T01:31:11-04:00,"Test Pattern Town, Test Pattern, TP",00121,株式会社スタジオジブリ,5012.123,5553.123,10565.246,1:11:11.123
2004-10-02T11:44:11-04:00,The Moon,00011,HERE WE GO,5012.123,5553.123,10565.246,
"""


def test_timestamp_parseable():
    assert csv_norm.norm_timestamp("4/1/11 11:00:00 AM") == "2011-04-01T14:00:00-04:00"


def test_timestamp_parseable_leading_zeroes():
    assert (
        csv_norm.norm_timestamp("04/01/11 11:00:00 AM") == "2011-04-01T14:00:00-04:00"
    )


def test_timestamp_parseable_no_leading_zero_hour():
    assert csv_norm.norm_timestamp("04/01/11 1:00:00 AM") == "2011-04-01T04:00:00-04:00"


def test_timestamp_unparseable():
    with pytest.raises(ValueError):
        csv_norm.norm_timestamp("4/1/11 11:00:00")


def test_zipcode_padding():
    assert csv_norm.norm_zipcode("234") == "00234"


def test_zipcode_no_padding():
    assert csv_norm.norm_zipcode("12345") == "12345"


def test_empty_csv():
    input_csv = io.StringIO()
    output_csv = io.StringIO()
    with pytest.raises(ValueError):
        csv_norm.main(input_csv, output_csv)


def test_norm_name():
    assert csv_norm.norm_name("Foo") == "FOO"


def test_norm_name_upper():
    assert csv_norm.norm_name("FOO") == "FOO"


def test_norm_name_non_latin():
    assert csv_norm.norm_name("株式会社スタジオジブリ") == "株式会社スタジオジブリ"


def test_norm_name_diaresis():
    assert csv_norm.norm_name("ülrich") == "ÜLRICH"


def test_duration_good():
    assert csv_norm.norm_duration("11:03:12.456") == 39792.456


def test_duration_bad():
    with pytest.raises(ValueError):
        csv_norm.norm_duration("11:03:12.asdf")


def test_good_csv():
    input_csv = io.StringIO(GOOD_CSV_INPUT, newline="\n")
    output_csv = io.StringIO(newline="\n")
    csv_norm.main(input_csv, output_csv)
    assert output_csv.getvalue() == GOOD_CSV_NORMALIZED
