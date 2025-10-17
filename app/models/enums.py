from enum import Enum


class LocationEnum(str, Enum):
    SEOUL = "서울"
    GYEONGGI = "경기"
    INCHEON = "인천"
    BUSAN = "부산"
    DAEGU = "대구"
    DAEJEON = "대전"
    GWANGJU = "광주"
    ULSAN = "울산"
    GANGWON = "강원"
    CHUNGBUK = "충북"
    CHUNGNAM = "충남"
    JEONBUK = "전북"
    JEONNAM = "전남"
    GYEONGBUK = "경북"
    GYEONGNAM = "경남"


class SalaryRangeEnum(str, Enum):
    NEGOTIABLE = "연봉 추후 협상"
    RANGE_20_30 = "2000만 ~ 3000만"
    RANGE_30_40 = "3000만 ~ 4000만"
    RANGE_40_50 = "4000만 ~ 5000만"
    RANGE_50_60 = "5000만 ~ 6000만"
    RANGE_60_70 = "6000만 ~ 7000만"
    RANGE_70_80 = "7000만 ~ 8000만"
    RANGE_80_90 = "8000만 ~ 9000만"
    RANGE_90_100 = "9000만 ~ 1억"
    RANGE_100_120 = "1억 ~ 1.2억"
    RANGE_120_150 = "1.2억 ~ 1.5억"
    OVER_150 = "1.5억 이상"


class EmploymentTypeEnum(str, Enum):
    FULL_TIME = "정규직"
    CONTRACT = "계약직"
    PART_TIME = "파견직"
    INTERN = "인턴"
    OTHER = "기타"
