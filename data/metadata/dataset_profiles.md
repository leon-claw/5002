# Dataset profiling for CityU 5002 group project

Generated from the downloaded files in `data/raw/` and `data/processed/`. The raw files are kept unchanged.

## College Majors 2026: earnings, debt, jobs and AI

- Source: Kaggle: kylefengkfeng209/college-majors-2026-earnings-debt-jobs-ai
- Local file: `data/processed/college-majors/college_majors_2026.csv`
- Shape: **227,980 rows × 72 columns**
- Size: 120.49 MB; duplicate rows: 0; missing cells: 27.79%

### Schema

| Column | Type | Non-null / unique or range |
|---|---|---|
| `program_id` | `object` | 227,980 unique incl. NA; top: opeid031505-51.07-1 (1), 230597-51.08-1 (1), 230597-47.06-1 (1) |
| `unitid` | `float64` | 220,960 non-null; min 100654.0; median 186876.0; max 499723.0; 6,127 unique |
| `opeid6` | `int64` | 227,980 non-null; min 1002; median 3116.0; max 43098; 6,033 unique |
| `institution_name` | `object` | 6,774 unique incl. NA; top: Pennsylvania State University-Main… (489), University of Minnesota-Twin Cities (477), Arizona State University Campus Im… (475) |
| `institution_control` | `object` | 4 unique incl. NA; top: Public (137,326), Private, nonprofit (72,513), Private, for-profit (13,479) |
| `is_main_campus` | `int64` | 227,980 non-null; min 0; median 1.0; max 1; 2 unique |
| `institution_city` | `object` | 2,223 unique incl. NA; top: None (11,296), New York (2,340), Chicago (2,020) |
| `institution_state` | `object` | 60 unique incl. NA; top: CA (21,264), NY (12,921), TX (12,001) |
| `institution_region` | `object` | 11 unique incl. NA; top: Southeast (48,897), Great Lakes (34,023), Mid East (33,923) |
| `institution_latitude` | `float64` | 216,684 non-null; min -14.322636; median 39.188648; max 71.324702; 5,623 unique |
| `institution_longitude` | `float64` | 216,684 non-null; min -170.742774; median -86.804805; max 171.378129; 5,623 unique |
| `institution_is_hbcu` | `float64` | 216,684 non-null; min 0.0; median 0.0; max 1.0; 2 unique |
| `institution_admission_rate` | `float64` | 133,060 non-null; min 0.0; median 0.7724; max 1.0; 1,514 unique |
| `institution_avg_sat` | `float64` | 100,152 non-null; min 720.0; median 1193.0; max 1560.0; 433 unique |
| `institution_undergrad_enrollment` | `float64` | 214,967 non-null; min 0.0; median 4304.0; max 163164.0; 2,701 unique |
| `institution_tuition_in_state_usd` | `float64` | 204,400 non-null; min 0.0; median 11221.0; max 72097.0; 2,673 unique |
| `institution_tuition_out_state_usd` | `float64` | 204,400 non-null; min 0.0; median 21700.0; max 72097.0; 2,720 unique |
| `cip_code_4digit` | `float64` | 227,980 non-null; min 1.0; median 39.07; max 61.26; 429 unique |
| `cip_title` | `object` | 429 unique incl. NA; top: Business Administration, Managemen… (6,621), Registered Nursing, Nursing Admini… (4,750), Accounting and Related Services (4,171) |
| `cip_family_code` | `int64` | 227,980 non-null; min 1; median 39.0; max 61; 49 unique |
| `cip_family_title` | `object` | 49 unique incl. NA; top: Health Professions and Related Pro… (31,325), Business, Management, Marketing, a… (27,515), Education (17,147) |
| `credential_level` | `int64` | 227,980 non-null; min 1; median 3.0; max 99; 9 unique |
| `credential_name` | `object` | 9 unique incl. NA; top: Bachelor's Degree (71,664), Undergraduate Certificate or Diplo… (43,465), Associate's Degree (42,373) |
| `distance_education` | `object` | 4 unique incl. NA; top: No credentials fully online (158,101), Not reported to IPEDS (28,906), All credentials fully online (23,380) |
| `awards_year1` | `float64` | 197,362 non-null; min 0.0; median 7.0; max 8584.0; 1,049 unique |
| `awards_year2` | `float64` | 199,074 non-null; min 0.0; median 7.0; max 7786.0; 1,037 unique |
| `outcomes_shared_across_campuses` | `int64` | 227,980 non-null; min 0; median 0.0; max 1; 2 unique |
| `median_earnings_4yr_usd` | `float64` | 58,112 non-null; min 6917.0; median 59018.5; max 336392.0; 38,164 unique |
| `earnings_cohort_size_4yr` | `float64` | 58,112 non-null; min 16.0; median 43.0; max 9665.0; 921 unique |
| `national_median_earnings_4yr_usd` | `float64` | 157,182 non-null; min 13421.0; median 57584.0; max 327492.0; 1,590 unique |
| `national_p25_earnings_4yr_usd` | `float64` | 156,376 non-null; min 7603.0; median 40535.0; max 175823.0; 1,490 unique |
| `national_p75_earnings_4yr_usd` | `float64` | 156,729 non-null; min 28852.0; median 77509.0; max 443362.0; 1,530 unique |
| `earnings_vs_national_pct` | `float64` | 58,108 non-null; min -86.6; median -1.0; max 412.0; 1,744 unique |
| `median_earnings_1yr_usd` | `float64` | 52,226 non-null; min 4506.0; median 43823.0; max 332843.0; 34,252 unique |
| `earnings_cohort_size_1yr` | `float64` | 52,226 non-null; min 16.0; median 42.0; max 11263.0; 866 unique |
| `median_earnings_5yr_usd` | `float64` | 50,512 non-null; min 7826.0; median 56269.5; max 384547.0; 34,334 unique |
| `earnings_cohort_size_5yr` | `float64` | 50,512 non-null; min 16.0; median 42.0; max 10468.0; 843 unique |
| `not_working_count_5yr` | `float64` | 137,509 non-null; min 0.0; median 1.0; max 1550.0; 226 unique |
| `count_above_hs_threshold_5yr` | `float64` | 43,836 non-null; min 16.0; median 39.0; max 8674.0; 702 unique |
| `count_working_in_state_5yr` | `float64` | 38,997 non-null; min 16.0; median 38.0; max 2990.0; 629 unique |
| `median_debt_usd` | `float64` | 46,673 non-null; min 1287.0; median 22630.0; max 459525.0; 16,631 unique |
| `debt_borrower_count` | `float64` | 58,101 non-null; min 10.0; median 33.0; max 11023.0; 876 unique |
| `median_monthly_payment_usd` | `float64` | 46,673 non-null; min 14.0; median 241.0; max 5227.0; 1,845 unique |
| `earnings_growth_pct_1yr_to_5yr` | `float64` | 39,121 non-null; min -60.82; median 30.14; max 1000.3; 11,761 unique |
| `earnings_trajectory_category` | `object` | 5 unique incl. NA; top: None (188,859), steep (17,080), steady (11,878) |
| `debt_to_earnings_1yr` | `float64` | 43,308 non-null; min 0.038; median 0.516; max 10.642; 2,274 unique |
| `debt_to_earnings_4yr` | `float64` | 43,375 non-null; min 0.028; median 0.36; max 5.757; 1,740 unique |
| `payment_to_income_pct_1yr` | `float64` | 43,308 non-null; min 0.48; median 6.66; max 145.28; 2,779 unique |
| `pct_above_hs_threshold_5yr` | `float64` | 43,836 non-null; min 14.6; median 86.7; max 118.8; 827 unique |
| `pct_working_5yr` | `float64` | 50,512 non-null; min 39.0; median 94.2; max 100.0; 429 unique |
| `pct_working_in_state_5yr` | `float64` | 38,997 non-null; min 1.5; median 80.0; max 112.5; 966 unique |
| `linked_occupations_count` | `float64` | 227,950 non-null; min 1.0; median 8.0; max 44.0; 26 unique |
| `linked_occupations_in_bls` | `float64` | 227,950 non-null; min 0.0; median 7.0; max 42.0; 25 unique |
| `largest_linked_occupation` | `object` | 133 unique incl. NA; top: Managers, all other (28,413), Secondary school teachers, except … (21,275), General and operations managers (14,390) |
| `largest_linked_occupation_soc` | `object` | 133 unique incl. NA; top: 11-9199 (28,413), 25-2031 (21,275), 11-1021 (14,390) |
| `occupation_typical_entry_education` | `object` | 8 unique incl. NA; top: Bachelor's degree (152,460), High school diploma or equivalent (23,780), Doctoral or professional degree (18,172) |
| `occupation_employment_2024_thousands` | `float64` | 222,452 non-null; min 1.6; median 1488.6; max 20634.0; 352 unique |
| `occupation_growth_pct_2024_34` | `float64` | 222,452 non-null; min -28.15; median 4.1; max 21.07; 308 unique |
| `occupation_growth_pct_max` | `float64` | 222,452 non-null; min -25.9; median 8.7; max 49.9; 99 unique |
| `occupation_annual_openings_thousands` | `float64` | 222,452 non-null; min 0.1; median 118.4; max 1753.3; 319 unique |
| `occupation_median_wage_2024_usd` | `float64` | 222,452 non-null; min 37320.0; median 80604.0; max 229046.0; 352 unique |
| `linked_occupations_in_onet` | `float64` | 227,950 non-null; min 0.0; median 7.0; max 42.0; 26 unique |
| `occupations_using_ai_software` | `float64` | 227,950 non-null; min 0.0; median 0.0; max 8.0; 9 unique |
| `ai_software_occupation_share` | `float64` | 218,368 non-null; min 0.0; median 0.0; max 1.0; 32 unique |
| `expert_system_occupation_share` | `float64` | 218,368 non-null; min 0.0; median 0.0; max 1.0; 39 unique |
| `ai_tools_max_per_occupation` | `float64` | 218,368 non-null; min 0.0; median 0.0; max 10.0; 7 unique |
| `hot_technologies_mean_per_occupation` | `float64` | 218,368 non-null; min 2.0; median 16.0; max 149.0; 237 unique |
| `ai_tool_examples` | `object` | 40 unique incl. NA; top: None (153,550), Neural network modeling software; … (12,372), Chatbot software (10,959) |
| `earnings_4yr_status` | `object` | 2 unique incl. NA; top: privacy_suppressed (169,868), reported (58,112) |
| `earnings_1yr_status` | `object` | 3 unique incl. NA; top: privacy_suppressed (156,343), reported (52,226), not_available (19,411) |
| `earnings_5yr_status` | `object` | 3 unique incl. NA; top: privacy_suppressed (158,057), reported (50,512), not_available (19,411) |
| `debt_status` | `object` | 3 unique incl. NA; top: privacy_suppressed (157,429), reported (46,673), not_available (23,878) |

### Missingness hotspots

| Column | Missing | Missing % |
|---|---:|---:|
| `count_working_in_state_5yr` | 188,983 | 82.89% |
| `pct_working_in_state_5yr` | 188,983 | 82.89% |
| `earnings_trajectory_category` | 188,859 | 82.84% |
| `earnings_growth_pct_1yr_to_5yr` | 188,859 | 82.84% |
| `payment_to_income_pct_1yr` | 184,672 | 81.00% |
| `debt_to_earnings_1yr` | 184,672 | 81.00% |
| `debt_to_earnings_4yr` | 184,605 | 80.97% |
| `count_above_hs_threshold_5yr` | 184,144 | 80.77% |
| `pct_above_hs_threshold_5yr` | 184,144 | 80.77% |
| `median_debt_usd` | 181,307 | 79.53% |
| `median_monthly_payment_usd` | 181,307 | 79.53% |
| `pct_working_5yr` | 177,468 | 77.84% |

---

## Spotify tracks and audio features (50k)

- Source: Kaggle: lorenzoscaturchio/spotify-tracks-audio-features-50k
- Local file: `data/processed/spotify/spotify_tracks.csv`
- Shape: **50,000 rows × 21 columns**
- Size: 12.73 MB; duplicate rows: 0; missing cells: 0.00%

### Schema

| Column | Type | Non-null / unique or range |
|---|---|---|
| `track_id` | `object` | 50,000 unique incl. NA; top: P3fAbnFbmOHnKYaXRvj7uf (1), dMsc6ZNnu0dvudf54kVoQl (1), CyZnVlzmpREfV0DCFwZI3Y (1) |
| `track_name` | `object` | 2,400 unique incl. NA; top: Silent Dance (85), Burning Fire (74), Silent Mountain (74) |
| `artist_name` | `object` | 415 unique incl. NA; top: Phantom Keys (1,098), Neon Pulse (1,061), The Drifters (1,046) |
| `album_name` | `object` | 481 unique incl. NA; top: Volume 3 (3,429), Volume 1 (3,369), Volume 2 (3,344) |
| `release_year` | `int64` | 50,000 non-null; min 2000; median 2017.0; max 2024; 25 unique |
| `genre` | `object` | 20 unique incl. NA; top: pop (6,786), hip-hop (5,810), rock (5,417) |
| `popularity` | `int64` | 50,000 non-null; min -5; median 19.0; max 100; 106 unique |
| `duration_ms` | `int64` | 50,000 non-null; min 90000; median 209886.5; max 403583; 42,848 unique |
| `explicit` | `bool` | 2 unique incl. NA; top: False (43,885), True (6,115) |
| `danceability` | `float64` | 50,000 non-null; min 0.0; median 0.6514861406502246; max 1.0; 49,057 unique |
| `energy` | `float64` | 50,000 non-null; min 0.0; median 0.6834793958942573; max 1.0; 47,942 unique |
| `loudness` | `float64` | 50,000 non-null; min -27.795903840048208; median -6.906656131426099; max 0.0; 48,891 unique |
| `speechiness` | `float64` | 50,000 non-null; min 0.0; median 0.0626085363436136; max 0.3684676586282327; 45,925 unique |
| `acousticness` | `float64` | 50,000 non-null; min 0.0; median 0.1989925715058016; max 1.0; 43,473 unique |
| `instrumentalness` | `float64` | 50,000 non-null; min 0.0; median 0.06452150528180664; max 1.0; 36,238 unique |
| `liveness` | `float64` | 50,000 non-null; min 0.0; median 0.1796833428441901; max 0.5819419097162825; 48,107 unique |
| `valence` | `float64` | 50,000 non-null; min 0.0; median 0.5811598083065592; max 1.0; 49,345 unique |
| `tempo` | `float64` | 50,000 non-null; min 50.0; median 115.32591101759493; max 220.0; 49,953 unique |
| `key` | `int64` | 50,000 non-null; min 0; median 5.0; max 11; 12 unique |
| `mode` | `int64` | 50,000 non-null; min 0; median 1.0; max 1; 2 unique |
| `time_signature` | `int64` | 50,000 non-null; min 3; median 4.0; max 7; 5 unique |

### Date/time candidates

- `release_year`: 50,000 valid; 2000 to 2024 (year)

---

## New York City Airbnb Open Data

- Source: Kaggle: dgomonov/new-york-city-airbnb-open-data
- Local file: `data/processed/airbnb/AB_NYC_2019.csv`
- Shape: **48,895 rows × 16 columns**
- Size: 6.75 MB; duplicate rows: 0; missing cells: 2.58%

### Schema

| Column | Type | Non-null / unique or range |
|---|---|---|
| `id` | `int64` | 48,895 non-null; min 2539; median 19677284.0; max 36487245; 48,895 unique |
| `name` | `object` | 47,906 unique incl. NA; top: Hillside Hotel (18), Home away from home (17), None (16) |
| `host_id` | `int64` | 48,895 non-null; min 2438; median 30793816.0; max 274321313; 37,457 unique |
| `host_name` | `object` | 11,453 unique incl. NA; top: Michael (417), David (403), Sonder (NYC) (327) |
| `neighbourhood_group` | `object` | 5 unique incl. NA; top: Manhattan (21,661), Brooklyn (20,104), Queens (5,666) |
| `neighbourhood` | `object` | 221 unique incl. NA; top: Williamsburg (3,920), Bedford-Stuyvesant (3,714), Harlem (2,658) |
| `latitude` | `float64` | 48,895 non-null; min 40.49979; median 40.72307; max 40.91306; 19,048 unique |
| `longitude` | `float64` | 48,895 non-null; min -74.24442; median -73.95568; max -73.71299; 14,718 unique |
| `room_type` | `object` | 3 unique incl. NA; top: Entire home/apt (25,409), Private room (22,326), Shared room (1,160) |
| `price` | `int64` | 48,895 non-null; min 0; median 106.0; max 10000; 674 unique |
| `minimum_nights` | `int64` | 48,895 non-null; min 1; median 3.0; max 1250; 109 unique |
| `number_of_reviews` | `int64` | 48,895 non-null; min 0; median 5.0; max 629; 394 unique |
| `last_review` | `object` | 1,765 unique incl. NA; top: None (10,052), 2019-06-23 (1,413), 2019-07-01 (1,359) |
| `reviews_per_month` | `float64` | 38,843 non-null; min 0.01; median 0.72; max 58.5; 937 unique |
| `calculated_host_listings_count` | `int64` | 48,895 non-null; min 1; median 1.0; max 327; 47 unique |
| `availability_365` | `int64` | 48,895 non-null; min 0; median 45.0; max 365; 366 unique |

### Missingness hotspots

| Column | Missing | Missing % |
|---|---:|---:|
| `last_review` | 10,052 | 20.56% |
| `reviews_per_month` | 10,052 | 20.56% |
| `host_name` | 21 | 0.04% |
| `name` | 16 | 0.03% |

---

## Student exam performance and success

- Source: Kaggle: mobeenfatimah/student-exam-performance-and-success-dataset
- Local file: `data/processed/student-exam/student_exam_performance.csv`
- Shape: **100,000 rows × 44 columns**
- Size: 24.56 MB; duplicate rows: 0; missing cells: 1.19%

### Schema

| Column | Type | Non-null / unique or range |
|---|---|---|
| `student_id` | `object` | 100,000 unique incl. NA; top: STU_000001 (1), STU_066651 (1), STU_066673 (1) |
| `age` | `int64` | 100,000 non-null; min 14; median 17.0; max 20; 7 unique |
| `gender` | `object` | 3 unique incl. NA; top: Male (49,130), Female (48,841), Other (2,029) |
| `education_level` | `object` | 2 unique incl. NA; top: High School (59,752), Undergraduate (40,248) |
| `school_type` | `object` | 3 unique incl. NA; top: Public (55,105), Private (34,916), Charter (9,979) |
| `family_income` | `object` | 5 unique incl. NA; top: Middle (30,112), Lower-Middle (25,066), Low (19,828) |
| `parent_education` | `object` | 6 unique incl. NA; top: High School (28,122), Bachelor (27,943), Associate (18,640) |
| `urban_rural` | `object` | 3 unique incl. NA; top: Urban (44,963), Suburban (35,141), Rural (19,896) |
| `previous_exam_score` | `float64` | 100,000 non-null; min 30.0; median 69.53; max 100.0; 6,153 unique |
| `previous_gpa` | `float64` | 92,207 non-null; min 1.0; median 2.78; max 4.0; 296 unique |
| `attendance_percentage` | `float64` | 90,137 non-null; min 46.34; median 84.75; max 100.0; 3,911 unique |
| `assignment_completion_rate` | `float64` | 100,000 non-null; min 20.0; median 69.57; max 100.0; 6,384 unique |
| `class_participation` | `object` | 3 unique incl. NA; top: Medium (50,109), Low (25,151), High (24,740) |
| `study_hours_per_day` | `float64` | 100,000 non-null; min 0.5; median 2.67; max 12.0; 1,073 unique |
| `self_study_hours` | `float64` | 100,000 non-null; min 0.25; median 1.84; max 10.0; 856 unique |
| `private_tuition` | `int64` | 100,000 non-null; min 0; median 0.0; max 1; 2 unique |
| `online_learning_hours` | `float64` | 100,000 non-null; min 0.0; median 1.38; max 15.0; 1,330 unique |
| `study_consistency` | `object` | 3 unique incl. NA; top: Medium (55,137), High (24,738), Low (20,125) |
| `study_environment` | `object` | 3 unique incl. NA; top: Quiet (49,789), Moderate (35,239), Noisy (14,972) |
| `study_method` | `object` | 5 unique incl. NA; top: Flashcards (20,239), Summarizing (20,048), Group Study (20,017) |
| `revision_frequency` | `object` | 3 unique incl. NA; top: Weekly (49,871), Daily (30,128), Rarely (20,001) |
| `practice_tests_completed` | `int64` | 100,000 non-null; min 0; median 5.0; max 20; 21 unique |
| `notes_quality` | `object` | 4 unique incl. NA; top: Average (54,973), Excellent (18,390), Poor (18,230) |
| `sleep_hours` | `float64` | 100,000 non-null; min 3.0; median 7.0; max 11.0; 793 unique |
| `sleep_quality` | `object` | 5 unique incl. NA; top: Fair (32,439), Good (32,380), Excellent (14,134) |
| `daily_screen_time` | `float64` | 100,000 non-null; min 1.0; median 4.99; max 12.08; 1,009 unique |
| `physical_activity_hours` | `float64` | 100,000 non-null; min 0.0; median 1.73; max 12.0; 1,197 unique |
| `break_frequency` | `object` | 3 unique incl. NA; top: Occasionally (49,866), Frequently (30,188), Rarely (19,946) |
| `stress_level` | `int64` | 100,000 non-null; min 5; median 10.0; max 10; 6 unique |
| `motivation_level` | `object` | 3 unique incl. NA; top: Medium (49,783), High (30,233), Low (19,984) |
| `internet_access` | `int64` | 100,000 non-null; min 0; median 1.0; max 1; 2 unique |
| `device_availability` | `object` | 3 unique incl. NA; top: Dedicated (71,862), Shared (25,173), None (2,965) |
| `educational_app_usage` | `object` | 3 unique incl. NA; top: Moderate (40,126), Low (39,961), High (19,913) |
| `online_course_hours` | `float64` | 100,000 non-null; min 0.0; median 2.08; max 20.0; 1,804 unique |
| `exam_difficulty` | `object` | 3 unique incl. NA; top: Medium (50,242), Hard (24,996), Easy (24,762) |
| `exam_preparation_days` | `int64` | 100,000 non-null; min 1; median 16.0; max 30; 30 unique |
| `questions_attempted` | `int64` | 100,000 non-null; min 85; median 92.0; max 100; 16 unique |
| `questions_correct` | `int64` | 100,000 non-null; min 0; median 57.0; max 100; 101 unique |
| `time_management_score` | `float64` | 90,387 non-null; min 17.03; median 79.0; max 100.0; 6,204 unique |
| `exam_anxiety_level` | `float64` | 100,000 non-null; min 1.0; median 9.49; max 10.0; 759 unique |
| `exam_score` | `float64` | 100,000 non-null; min 0.0; median 61.96; max 100.0; 8,086 unique |
| `performance_grade` | `object` | 5 unique incl. NA; top: D (34,886), F (22,611), C (21,794) |
| `pass_status` | `object` | 2 unique incl. NA; top: Pass (77,389), Fail (22,611) |
| `performance_level` | `object` | 3 unique incl. NA; top: Low (45,123), Medium (41,999), High (12,878) |

### Missingness hotspots

| Column | Missing | Missing % |
|---|---:|---:|
| `attendance_percentage` | 9,863 | 9.86% |
| `time_management_score` | 9,613 | 9.61% |
| `notes_quality` | 8,407 | 8.41% |
| `previous_gpa` | 7,793 | 7.79% |
| `sleep_quality` | 6,994 | 6.99% |
| `parent_education` | 6,526 | 6.53% |
| `device_availability` | 2,965 | 2.96% |

---

## NYC film permits (historical public mirror)

- Source: Public GitHub mirror of NYC MOME permits, 2011–2015
- Local file: `data/raw/nyc-film-permits-historical.csv`
- Shape: **40,754 rows × 11 columns**
- Size: 13.13 MB; duplicate rows: 136; missing cells: 0.28%

### Schema

| Column | Type | Non-null / unique or range |
|---|---|---|
| `ProjectTitle` | `object` | 3,326 unique incl. NA; top: Law and Order: SVU (376), GOOD MORNING AMERICA 2014 (373), Blue Bloods Season 3 (361) |
| `EventName` | `object` | 37,844 unique incl. NA; top: Scouting (62), Scouting Permit (39), Newlyweds Season One (27) |
| `EventType` | `object` | 7 unique incl. NA; top: Shooting Permit (34,835), Rigging Permit (5,105), DCAS Prep/Shoot/Wrap Permit (461) |
| `EventStartDate` | `object` | 14,377 unique incl. NA; top: 2015-02-23T07:00:00 (37), 2014-09-08T06:00:00 (31), 2014-12-01T06:00:00 (27) |
| `EventEndDate` | `object` | 17,705 unique incl. NA; top: 2015-02-23T21:00:00 (24), 2014-08-04T21:00:00 (19), 2014-08-12T22:00:00 (19) |
| `Location` | `object` | 26,660 unique incl. NA; top: BROADWAY between WEST 53 STREET an… (520), 1211 AVENUE OF THE AMERICAS betwee… (432), None (422) |
| `Boro` | `object` | 6 unique incl. NA; top: Manhattan (20,655), Brooklyn (11,465), Queens (6,255) |
| `ProjectId` | `int64` | 40,754 non-null; min 1; median 6824.0; max 14588; 3,371 unique |
| `CategoryName` | `object` | 2 unique incl. NA; top: Television (27,834), Film (12,920) |
| `SubCategoryName` | `object` | 21 unique incl. NA; top: Episodic series (11,902), Feature (8,282), Cable-episodic (4,508) |
| `CompanyName` | `object` | 2,246 unique incl. NA; top: Bonanza Productions Inc (718), NBCUniversal Media, LLC (675), Eye Productions Inc. (669) |

### Missingness hotspots

| Column | Missing | Missing % |
|---|---:|---:|
| `Boro` | 834 | 2.05% |
| `Location` | 422 | 1.04% |

### Date/time candidates

- `EventStartDate`: 40,754 valid; 2011-07-25 00:00:00 to 2015-08-04 13:00:00 (datetime)
- `EventEndDate`: 40,754 valid; 2011-11-01 01:00:00 to 2016-06-30 00:00:00 (datetime)

---

## World Happiness Report 2026, Figure 2.1 data

- Source: Official World Happiness Report data sharing page
- Local file: `data/raw/world-happiness-report-2026-figure-2-1.xlsx`
- Shape: **2,116 rows × 13 columns**
- Size: 0.13 MB; duplicate rows: 0; missing cells: 35.91%

### Schema

| Column | Type | Non-null / unique or range |
|---|---|---|
| `Year` | `int64` | 2,116 non-null; min 2011; median 2018.0; max 2025; 14 unique |
| `Rank` | `int64` | 2,116 non-null; min 1; median 76.0; max 158; 158 unique |
| `Country name` | `object` | 168 unique incl. NA; top: Finland (14), Indonesia (14), Nigeria (14) |
| `Life evaluation (3-year average)` | `float64` | 2,116 non-null; min 1.364; median 5.48; max 7.856; 1,673 unique |
| `Lower whisker` | `float64` | 1,022 non-null; min 1.301; median 5.59263120651245; max 7.78; 903 unique |
| `Upper whisker` | `float64` | 1,022 non-null; min 1.427; median 5.811999999999999; max 7.904; 927 unique |
| `Explained by: Log GDP per capita` | `float64` | 1,019 non-null; min 0.0; median 1.304; max 2.209; 802 unique |
| `Explained by: Social support` | `float64` | 1,019 non-null; min 0.0; median 1.14011859893799; max 1.84; 785 unique |
| `Explained by: Healthy life expectancy` | `float64` | 1,016 non-null; min 0.0; median 0.5605; max 1.238; 680 unique |
| `Explained by: Freedom to make life choices` | `float64` | 1,017 non-null; min 0.0; median 0.602; max 1.147; 668 unique |
| `Explained by: Generosity` | `float64` | 1,019 non-null; min 0.0; median 0.134; max 0.56981372833252; 436 unique |
| `Explained by: Perceptions of corruption` | `float64` | 1,018 non-null; min 0.0; median 0.113; max 0.587; 479 unique |
| `Dystopia + residual` | `float64` | 1,013 non-null; min -0.295; median 1.765; max 3.482; 869 unique |

### Missingness hotspots

| Column | Missing | Missing % |
|---|---:|---:|
| `Dystopia + residual` | 1,103 | 52.13% |
| `Explained by: Healthy life expectancy` | 1,100 | 51.98% |
| `Explained by: Freedom to make life choices` | 1,099 | 51.94% |
| `Explained by: Perceptions of corruption` | 1,098 | 51.89% |
| `Explained by: Log GDP per capita` | 1,097 | 51.84% |
| `Explained by: Social support` | 1,097 | 51.84% |
| `Explained by: Generosity` | 1,097 | 51.84% |
| `Lower whisker` | 1,094 | 51.70% |
| `Upper whisker` | 1,094 | 51.70% |

### Date/time candidates

- `Year`: 2,116 valid; 2011 to 2025 (year)

---

## 2018 Central Park Squirrel Census

- Source: NYC Open Data / TidyTuesday public mirror
- Local file: `data/raw/central-park-squirrel-census.csv`
- Shape: **3,023 rows × 31 columns**
- Size: 0.71 MB; duplicate rows: 0; missing cells: 13.02%

### Schema

| Column | Type | Non-null / unique or range |
|---|---|---|
| `X` | `float64` | 3,023 non-null; min -73.9811585807616; median -73.9685940262068; max -73.9497217674555; 3,023 unique |
| `Y` | `float64` | 3,023 non-null; min 40.7649106677138; median 40.7781658424866; max 40.8001185184892; 3,023 unique |
| `Unique Squirrel ID` | `object` | 3,018 unique incl. NA; top: 7D-PM-1010-01 (2), 40B-AM-1019-06 (2), 37E-PM-1006-03 (2) |
| `Hectare` | `object` | 339 unique incl. NA; top: 14D (32), 32E (30), 14E (28) |
| `Shift` | `object` | 2 unique incl. NA; top: PM (1,676), AM (1,347) |
| `Date` | `int64` | 3,023 non-null; min 10062018; median 10122018.0; max 10202018; 11 unique |
| `Hectare Squirrel Number` | `int64` | 3,023 non-null; min 1; median 3.0; max 23; 23 unique |
| `Age` | `object` | 4 unique incl. NA; top: Adult (2,568), Juvenile (330), None (121) |
| `Primary Fur Color` | `object` | 4 unique incl. NA; top: Gray (2,473), Cinnamon (392), Black (103) |
| `Highlight Fur Color` | `object` | 11 unique incl. NA; top: None (1,086), Cinnamon (767), White (585) |
| `Combination of Primary and Highlight Color` | `object` | 22 unique incl. NA; top: Gray+ (895), Gray+Cinnamon (752), Gray+White (489) |
| `Color notes` | `object` | 136 unique incl. NA; top: None (2,841), Gray & Cinnamon selected as Primar… (9), white belly (5) |
| `Location` | `object` | 3 unique incl. NA; top: Ground Plane (2,116), Above Ground (843), None (64) |
| `Above Ground Sighter Measurement` | `object` | 42 unique incl. NA; top: FALSE (2,116), 10 (116), None (114) |
| `Specific Location` | `object` | 305 unique incl. NA; top: None (2,547), tree (43), in tree (32) |
| `Running` | `bool` | 2 unique incl. NA; top: False (2,293), True (730) |
| `Chasing` | `bool` | 2 unique incl. NA; top: False (2,744), True (279) |
| `Climbing` | `bool` | 2 unique incl. NA; top: False (2,365), True (658) |
| `Eating` | `bool` | 2 unique incl. NA; top: False (2,263), True (760) |
| `Foraging` | `bool` | 2 unique incl. NA; top: False (1,588), True (1,435) |
| `Other Activities` | `object` | 308 unique incl. NA; top: None (2,586), digging (19), sitting (16) |
| `Kuks` | `bool` | 2 unique incl. NA; top: False (2,921), True (102) |
| `Quaas` | `bool` | 2 unique incl. NA; top: False (2,973), True (50) |
| `Moans` | `bool` | 2 unique incl. NA; top: False (3,020), True (3) |
| `Tail flags` | `bool` | 2 unique incl. NA; top: False (2,868), True (155) |
| `Tail twitches` | `bool` | 2 unique incl. NA; top: False (2,589), True (434) |
| `Approaches` | `bool` | 2 unique incl. NA; top: False (2,845), True (178) |
| `Indifferent` | `bool` | 2 unique incl. NA; top: False (1,569), True (1,454) |
| `Runs from` | `bool` | 2 unique incl. NA; top: False (2,345), True (678) |
| `Other Interactions` | `object` | 198 unique incl. NA; top: None (2,783), runs from (dog) (9), curious (6) |
| `Lat/Long` | `object` | 3,023 unique incl. NA; top: POINT (-73.9561344937861 40.794082… (1), POINT (-73.9691453885964 40.777052… (1), POINT (-73.9603245806655 40.794271… (1) |

### Missingness hotspots

| Column | Missing | Missing % |
|---|---:|---:|
| `Color notes` | 2,841 | 93.98% |
| `Other Interactions` | 2,783 | 92.06% |
| `Other Activities` | 2,586 | 85.54% |
| `Specific Location` | 2,547 | 84.25% |
| `Highlight Fur Color` | 1,086 | 35.92% |
| `Age` | 121 | 4.00% |
| `Above Ground Sighter Measurement` | 114 | 3.77% |
| `Location` | 64 | 2.12% |
| `Primary Fur Color` | 55 | 1.82% |

---

## Hong Kong beach water quality (2025)

- Source: Hong Kong Environmental Protection Department
- Local file: `data/raw/hong-kong-beach-historical-2025-tc.csv`
- Shape: **1,409 rows × 3 columns**
- Size: 0.05 MB; duplicate rows: 0; missing cells: 0.00%

### Schema

| Column | Type | Non-null / unique or range |
|---|---|---|
| `泳灘名稱` | `object` | 43 unique incl. NA; top: 更生灣泳灘 (45), 麗都灣泳灘 (45), 深水灣泳灘 (42) |
| `取樣日期(日日/月月/年年年年)` | `object` | 160 unique incl. NA; top: 02/10/2025 (26), 22/09/2025 (26), 28/05/2025 (22) |
| `取樣當天每百毫升大腸桿菌含量` | `int64` | 1,409 non-null; min 1; median 12.0; max 18000; 203 unique |

---

## Steam Games Dataset V2

- Source: Kaggle: muhammadaqeelkabir/steam-games-dataset-v2; extended table
- Local file: `data/processed/steam/extended_steam_games.csv`
- Shape: **23,100 rows × 28 columns**
- Size: 13.96 MB; duplicate rows: 489; missing cells: 3.16%

### Schema

| Column | Type | Non-null / unique or range |
|---|---|---|
| `appid` | `int64` | 23,100 non-null; min 10; median 927555.0; max 3738180; 22,608 unique |
| `name` | `object` | 22,542 unique incl. NA; top: Light (3), none (3), F.E.A.R. (3) |
| `developer` | `object` | 15,156 unique incl. NA; top: KOEI TECMO GAMES CO., LTD. (69), None (66), Square Enix (50) |
| `publisher` | `object` | 12,061 unique incl. NA; top: Ubisoft (135), Electronic Arts (134), None (133) |
| `positive` | `int64` | 23,100 non-null; min 0; median 286.0; max 7642084; 5,660 unique |
| `negative` | `int64` | 23,100 non-null; min 0; median 75.0; max 1173003; 2,816 unique |
| `owners` | `object` | 12 unique incl. NA; top: 20,000 .. 50,000 (8,067), 50,000 .. 100,000 (5,656), 100,000 .. 200,000 (3,658) |
| `average_forever` | `int64` | 23,100 non-null; min 0; median 0.0; max 0; 1 unique |
| `average_2weeks` | `int64` | 23,100 non-null; min 0; median 0.0; max 0; 1 unique |
| `median_forever` | `int64` | 23,100 non-null; min 0; median 0.0; max 0; 1 unique |
| `median_2weeks` | `int64` | 23,100 non-null; min 0; median 0.0; max 0; 1 unique |
| `price` | `int64` | 23,100 non-null; min 0; median 499.0; max 19999; 306 unique |
| `initialprice` | `int64` | 23,100 non-null; min 0; median 699.0; max 19999; 150 unique |
| `discount` | `int64` | 23,100 non-null; min 0; median 0.0; max 100; 60 unique |
| `ccu` | `int64` | 23,100 non-null; min 0; median 0.0; max 1013936; 1,102 unique |
| `release_date` | `object` | 5,276 unique incl. NA; top: None (102), Jan 28, 2021 (28), Apr 5, 2016 (25) |
| `required_age` | `float64` | 23,052 non-null; min 0.0; median 0.0; max 19.0; 14 unique |
| `is_free` | `object` | 3 unique incl. NA; top: False (20,047), True (3,005), None (48) |
| `short_description` | `object` | 22,434 unique incl. NA; top: None (67), Minimal physical puzzle with explo… (15), “What’s your sign, baby?” - Larry … (7) |
| `supported_languages` | `object` | 8,282 unique incl. NA; top: English (4,328), English<strong>*</strong><br><stro… (4,214), English, Russian (346) |
| `platforms_windows` | `object` | 3 unique incl. NA; top: True (23,046), None (48), False (6) |
| `platforms_mac` | `object` | 3 unique incl. NA; top: False (16,864), True (6,188), None (48) |
| `platforms_linux` | `object` | 3 unique incl. NA; top: False (18,881), True (4,171), None (48) |
| `metacritic_score` | `float64` | 3,706 non-null; min 20.0; median 76.0; max 97.0; 70 unique |
| `recommendations` | `float64` | 23,052 non-null; min 0.0; median 202.0; max 5211693.0; 5,305 unique |
| `achievements` | `float64` | 23,052 non-null; min 0.0; median 14.0; max 9821.0; 371 unique |
| `genres` | `object` | 1,402 unique incl. NA; top: Action, Indie (1,241), Action, Adventure, Indie (1,075), Adventure, Indie (1,058) |
| `categories` | `object` | 5,648 unique incl. NA; top: Single-player, Family Sharing (3,128), Single-player, Steam Achievements,… (1,347), Single-player, Steam Achievements,… (694) |

### Missingness hotspots

| Column | Missing | Missing % |
|---|---:|---:|
| `metacritic_score` | 19,394 | 83.96% |
| `categories` | 148 | 0.64% |
| `publisher` | 133 | 0.58% |
| `genres` | 109 | 0.47% |
| `release_date` | 102 | 0.44% |
| `short_description` | 67 | 0.29% |
| `developer` | 66 | 0.29% |
| `supported_languages` | 63 | 0.27% |
| `required_age` | 48 | 0.21% |
| `is_free` | 48 | 0.21% |
| `platforms_windows` | 48 | 0.21% |
| `platforms_mac` | 48 | 0.21% |

---

## Steam Games Dataset V2 — Wikidata enrichment table

- Source: Kaggle: muhammadaqeelkabir/steam-games-dataset-v2
- Local file: `data/processed/steam/steam_games_wikidata.csv`
- Shape: **128,348 rows × 8 columns**
- Size: 6.09 MB; duplicate rows: 0; missing cells: 60.68%

### Schema

| Column | Type | Non-null / unique or range |
|---|---|---|
| `appid` | `int64` | 128,348 non-null; min 10; median 1858080.0; max 5005310; 128,348 unique |
| `wikidata_name` | `object` | 127,136 unique incl. NA; top: Entropy (5), Labyrinth (5), Alone (5) |
| `esrb_rating` | `object` | 13 unique incl. NA; top: None (121,836), Teen (2,142), Everyone (1,628) |
| `hltb_id` | `float64` | 1 non-null; min 1455517844.0; median 1455517844.0; max 1455517844.0; 1 unique |
| `igdb_id` | `object` | 116,542 unique incl. NA; top: None (11,603), girls-frontline (3), automon (2) |
| `metacritic_id` | `float64` |  |
| `opencritic_id` | `float64` | 13,252 non-null; min 15.0; median 11859.5; max 20897.0; 13,232 unique |
| `game_engine` | `object` | 426 unique incl. NA; top: None (117,846), Q63966 (5,129), Unreal Engine 4 (1,270) |

### Missingness hotspots

| Column | Missing | Missing % |
|---|---:|---:|
| `metacritic_id` | 128,348 | 100.00% |
| `hltb_id` | 128,347 | 100.00% |
| `esrb_rating` | 121,836 | 94.93% |
| `game_engine` | 117,846 | 91.82% |
| `opencritic_id` | 115,096 | 89.67% |
| `igdb_id` | 11,603 | 9.04% |
| `wikidata_name` | 1 | 0.00% |

---

## Steam Games Dataset V2 — SteamSpy raw table

- Source: Kaggle: muhammadaqeelkabir/steam-games-dataset-v2
- Local file: `data/processed/steam/steamspy_raw.csv`
- Shape: **30,000 rows × 15 columns**
- Size: 3.04 MB; duplicate rows: 1,166; missing cells: 0.06%

### Schema

| Column | Type | Non-null / unique or range |
|---|---|---|
| `appid` | `int64` | 30,000 non-null; min 10; median 1033755.0; max 3738180; 28,834 unique |
| `name` | `object` | 28,746 unique incl. NA; top: Bounce (6), Light (3), RIP - Trilogy (3) |
| `developer` | `object` | 19,229 unique incl. NA; top: None (86), KOEI TECMO GAMES CO., LTD. (81), Square Enix (51) |
| `publisher` | `object` | 15,580 unique incl. NA; top: None (186), Ubisoft (140), SEGA (136) |
| `positive` | `int64` | 30,000 non-null; min 0; median 162.0; max 7642084; 5,662 unique |
| `negative` | `int64` | 30,000 non-null; min 0; median 44.0; max 1173003; 2,816 unique |
| `owners` | `object` | 13 unique incl. NA; top: 20,000 .. 50,000 (11,941), 50,000 .. 100,000 (5,656), 100,000 .. 200,000 (3,658) |
| `average_forever` | `int64` | 30,000 non-null; min 0; median 0.0; max 0; 1 unique |
| `average_2weeks` | `int64` | 30,000 non-null; min 0; median 0.0; max 0; 1 unique |
| `median_forever` | `int64` | 30,000 non-null; min 0; median 0.0; max 0; 1 unique |
| `median_2weeks` | `int64` | 30,000 non-null; min 0; median 0.0; max 0; 1 unique |
| `price` | `int64` | 30,000 non-null; min 0; median 499.0; max 19999; 342 unique |
| `initialprice` | `int64` | 30,000 non-null; min 0; median 599.0; max 19999; 172 unique |
| `discount` | `int64` | 30,000 non-null; min 0; median 0.0; max 100; 64 unique |
| `ccu` | `int64` | 30,000 non-null; min 0; median 0.0; max 1013936; 1,105 unique |

### Missingness hotspots

| Column | Missing | Missing % |
|---|---:|---:|
| `publisher` | 186 | 0.62% |
| `developer` | 86 | 0.29% |
| `name` | 1 | 0.00% |

---

## NASA Exoplanet Archive Planetary Systems table

- Source: NASA Exoplanet Archive TAP, table ps
- Local file: `data/raw/nasa-exoplanets-ps.csv`
- Shape: **40,155 rows × 355 columns**
- Size: 132.41 MB; duplicate rows: 56; missing cells: 46.65%

### Schema

| Column | Type | Non-null / unique or range |
|---|---|---|
| `pl_name` | `object` | 6,366 unique incl. NA; top: TrES-2 b (34), Kepler-10 b (25), HAT-P-7 b (24) |
| `pl_letter` | `object` | 8 unique incl. NA; top: b (29,042), c (7,168), d (2,622) |
| `hostname` | `object` | 4,775 unique incl. NA; top: Kepler-11 (103), Kepler-80 (95), Kepler-32 (91) |
| `hd_name` | `object` | 751 unique incl. NA; top: None (37,042), HD 75732 (66), HD 3167 (34) |
| `hip_name` | `object` | 801 unique incl. NA; top: None (36,714), HIP 43587 (66), HIP 94931 (50) |
| `tic_id` | `object` | 4,483 unique incl. NA; top: None (840), TIC 169175503 (103), TIC 184296619 (95) |
| `gaia_dr2_id` | `object` | 4,440 unique incl. NA; top: None (1,147), Gaia DR2 2076960598545789824 (103), Gaia DR2 2076328963475704576 (95) |
| `gaia_dr3_id` | `object` | 4,413 unique incl. NA; top: None (1,392), Gaia DR3 2076960598545789824 (103), Gaia DR3 2076328963475704576 (95) |
| `default_flag` | `int64` | 40,155 non-null; min 0; median 0.0; max 1; 2 unique |
| `pl_refname` | `object` | 2,712 unique incl. NA; top: <a refstr=Q1_Q17_DR25_SUPPLEMENTAL… (2,736), <a refstr=Q1_Q16_KOI_TABLE href=ht… (2,723), <a refstr=Q1_Q17_DR25_KOI_TABLE hr… (2,719) |
| `sy_refname` | `object` | 223 unique incl. NA; top: <a refstr=STASSUN_ET_AL__2019 href… (39,299), <a refstr=ZANG_ET_AL__2023 href=ht… (28), <a refstr=HWANG_ET_AL__2022 href=h… (26) |
| `disc_pubdate` | `object` | 302 unique incl. NA; top: 2016-05 (12,359), 2014-03 (8,785), 2022-02 (2,425) |
| `disc_year` | `int64` | 40,155 non-null; min 1992; median 2016.0; max 2026; 34 unique |
| `discoverymethod` | `object` | 11 unique incl. NA; top: Transit (36,073), Radial Velocity (2,952), Microlensing (821) |
| `disc_locale` | `object` | 4 unique incl. NA; top: Space (33,343), Ground (6,735), Multiple Locales (74) |
| `disc_facility` | `object` | 73 unique incl. NA; top: Kepler (28,592), Transiting Exoplanet Survey Satell… (2,397), K2 (2,168) |
| `disc_instrument` | `object` | 103 unique incl. NA; top: Kepler CCD Array (30,760), TESS CCD Array (2,397), iKon-L CCD Camera (1,218) |
| `disc_telescope` | `object` | 84 unique incl. NA; top: 0.95 m Kepler Telescope (30,760), 0.1 m TESS Telescope (2,397), Canon 200mm f/1.8L (1,882) |
| `disc_refname` | `object` | 1,751 unique incl. NA; top: <a refstr=MORTON_ET_AL__2016 href=… (12,326), <a refstr=ROWE_ET_AL__2014 href=ht… (8,656), <a refstr=VALIZADEGAN_ET_AL__2022 … (2,318) |
| `ra` | `float64` | 40,155 non-null; min 0.1856063; median 289.3473634; max 359.9749837; 4,785 unique |
| `rastr` | `object` | 4,772 unique incl. NA; top: 19h48m27.62s (103), 19h44m27.02s (95), 19h51m22.15s (91) |
| `dec` | `float64` | 40,155 non-null; min -89.4715133; median 42.4753193; max 88.8298759; 4,780 unique |
| `decstr` | `object` | 4,782 unique incl. NA; top: +41d54m32.79s (103), +39d58m43.48s (95), +46d34m27.69s (91) |
| `glon` | `float64` | 40,155 non-null; min 0.02901; median 77.59797; max 359.99627; 4,776 unique |
| `glat` | `float64` | 40,155 non-null; min -88.32478; median 12.75373; max 89.52659; 4,777 unique |
| `elon` | `float64` | 40,155 non-null; min 0.36673; median 304.38216; max 359.8973; 4,778 unique |
| `elat` | `float64` | 40,155 non-null; min -88.60569; median 62.82858; max 87.12854; 4,776 unique |
| `pl_orbper` | `float64` | 36,771 non-null; min 0.090706293; median 10.30400497; max 402000000.0; 23,805 unique |
| `pl_orbpererr1` | `float64` | 35,035 non-null; min 0.0; median 3.824e-05; max 470000000.0; 10,375 unique |
| `pl_orbpererr2` | `float64` | 35,034 non-null; min -100000000.0; median -3.8269500000000003e-05; max 0.0; 10,372 unique |
| `pl_orbperlim` | `float64` | 36,771 non-null; min -1.0; median 0.0; max 1.0; 3 unique |
| `pl_orbperstr` | `object` | 25,888 unique incl. NA; top: None (3,384), 4.9546416&plusmn;0.0000035 (6), 0.35500744&plusmn;0.00000006 (5) |
| `pl_orblpererr1` | `float64` | 3,352 non-null; min 0.0; median 23.0; max 354.3; 1,024 unique |
| `pl_orblper` | `float64` | 3,811 non-null; min -233.0; median 98.0; max 395.341; 1,830 unique |
| `pl_orblpererr2` | `float64` | 3,352 non-null; min -423.5; median -22.0; max 0.0; 1,000 unique |
| `pl_orblperlim` | `float64` | 19,680 non-null; min -1.0; median 0.0; max 0.0; 2 unique |
| `pl_orblperstr` | `object` | 3,383 unique incl. NA; top: None (36,344), 90 (234), 0 (95) |
| `pl_orbsmax` | `float64` | 22,410 non-null; min 0.0044; median 0.1015; max 19000.0; 6,618 unique |
| `pl_orbsmaxerr1` | `float64` | 7,926 non-null; min 0.0; median 0.002; max 5205.0; 1,025 unique |
| `pl_orbsmaxerr2` | `float64` | 7,925 non-null; min -2060.0; median -0.002; max 0.0; 1,014 unique |
| `pl_orbsmaxlim` | `float64` | 25,198 non-null; min -1.0; median 0.0; max 0.0; 2 unique |
| `pl_orbsmaxstr` | `object` | 10,752 unique incl. NA; top: None (17,745), .06 (48), .052 (45) |
| `pl_orbincl` | `float64` | 17,812 non-null; min -39.93; median 88.81; max 178.3; 1,999 unique |
| `pl_orbinclerr1` | `float64` | 4,514 non-null; min 0.0; median 0.5; max 63.943; 925 unique |
| `pl_orbinclerr2` | `float64` | 4,516 non-null; min -89.0; median -0.5; max 0.0; 924 unique |
| `pl_orbincllim` | `float64` | 20,557 non-null; min -1.0; median 0.0; max 1.0; 3 unique |
| `pl_orbinclstr` | `object` | 4,729 unique incl. NA; top: None (22,343), 89.95 (3,363), 89.38 (2,300) |
| `pl_orbtper` | `float64` | 1,821 non-null; min 2173967.5; median 2454343.12; max 2504701.0; 1,753 unique |
| `pl_orbtpererr1` | `float64` | 1,764 non-null; min 0.0; median 12.0; max 32872.5; 884 unique |
| `pl_orbtpererr2` | `float64` | 1,764 non-null; min -87171.695; median -12.0; max 0.0; 873 unique |
| `pl_orbtperlim` | `float64` | 1,821 non-null; min 0.0; median 0.0; max 0.0; 1 unique |
| `pl_orbtperstr` | `object` | 1,792 unique incl. NA; top: None (38,334), 2450602.093 (4), <div><span class=supersubNumber">2… (3) |
| `pl_orbeccen` | `float64` | 19,119 non-null; min -0.011; median 0.0; max 0.97; 1,005 unique |
| `pl_orbeccenerr1` | `float64` | 4,013 non-null; min 0.0; median 0.04; max 0.62; 389 unique |
| `pl_orbeccenerr2` | `float64` | 4,012 non-null; min -0.703; median -0.034; max 0.0; 369 unique |
| `pl_orbeccenlim` | `float64` | 21,864 non-null; min -1.0; median 0.0; max 9.0; 4 unique |
| `pl_orbeccenstr` | `object` | 3,704 unique incl. NA; top: None (21,036), 0 (14,219), 0.0 (127) |
| `pl_eqt` | `float64` | 17,649 non-null; min 34.0; median 799.0; max 4050.0; 3,161 unique |
| `pl_eqterr1` | `float64` | 2,770 non-null; min 0.0; median 21.0; max 1217.0; 394 unique |
| `pl_eqterr2` | `float64` | 2,770 non-null; min -1217.0; median -20.0; max -0.32; 392 unique |
| `pl_eqtlim` | `float64` | 20,394 non-null; min 0.0; median 0.0; max 1.0; 2 unique |
| `pl_eqtstr` | `object` | 5,295 unique incl. NA; top: None (22,506), 767 (39), 583 (33) |
| `pl_occdep` | `float64` | 50 non-null; min 0.00065; median 0.009219999999999999; max 90.81; 49 unique |
| `pl_occdeperr1` | `float64` | 47 non-null; min 6.6e-05; median 0.0014; max 1.01; 39 unique |
| `pl_occdeperr2` | `float64` | 47 non-null; min -1.01; median -0.0014; max -6.4e-05; 38 unique |
| `pl_occdeplim` | `float64` | 50 non-null; min 0.0; median 0.0; max 1.0; 2 unique |
| `pl_occdepstr` | `object` | 51 unique incl. NA; top: None (40,105), <div><span class=supersubNumber">0… (1), 0.0035&plusmn;0.0018 (1) |
| `pl_insol` | `float64` | 17,423 non-null; min 0.0003; median 86.5; max 58192.75; 9,759 unique |
| `pl_insolerr1` | `float64` | 15,894 non-null; min 0.0; median 27.0; max 48504.39; 7,006 unique |
| `pl_insolerr2` | `float64` | 15,894 non-null; min -28302.96; median -13.52; max 0.0; 6,306 unique |
| `pl_insollim` | `float64` | 22,485 non-null; min 0.0; median 0.0; max 0.0; 1 unique |
| `pl_insolstr` | `object` | 11,952 unique incl. NA; top: None (22,732), 2.6&plusmn;0.2 (6), 3.9&plusmn;0.3 (5) |
| `pl_dens` | `float64` | 2,923 non-null; min 0.00074; median 1.31; max 2331.0; 1,301 unique |
| `pl_denserr1` | `float64` | 2,781 non-null; min 0.00055; median 0.26; max 50000.0; 632 unique |
| `pl_denserr2` | `float64` | 2,781 non-null; min -2316.0; median -0.24; max -0.00023; 593 unique |
| `pl_denslim` | `float64` | 2,923 non-null; min -1.0; median 0.0; max 9.0; 4 unique |
| `pl_densstr` | `object` | 2,846 unique incl. NA; top: None (37,232), &lt;3.0 (4), 0.8&plusmn;0.1 (4) |
| `pl_trandep` | `float64` | 18,327 non-null; min 0.00119; median 0.06; max 56.65; 7,915 unique |
| `pl_trandeperr1` | `float64` | 13,741 non-null; min 1.25e-06; median 0.00182; max 2967.072; 2,367 unique |
| `pl_trandeperr2` | `float64` | 13,741 non-null; min -2967.072; median -0.00182; max -1.25e-06; 2,356 unique |
| `pl_trandeplim` | `float64` | 21,072 non-null; min -1.0; median 0.0; max 0.0; 2 unique |
| `pl_trandepstr` | `object` | 10,981 unique incl. NA; top: None (21,828), 0.02670 (9), 0.02510 (7) |
| `pl_tranmid` | `float64` | 31,209 non-null; min 2405150.39051; median 2454985.12282; max 2462735.0; 20,496 unique |
| `pl_tranmiderr1` | `float64` | 30,716 non-null; min 0.0; median 0.002393295; max 15000.0; 7,265 unique |
| `pl_tranmiderr2` | `float64` | 30,716 non-null; min -4500.0; median -0.00239; max 0.0; 7,277 unique |
| `pl_tranmidlim` | `float64` | 31,209 non-null; min 0.0; median 0.0; max 0.0; 1 unique |
| `pl_tranmidstr` | `object` | 22,894 unique incl. NA; top: None (8,946), 2455104.088&plusmn;0.00125 (5), 2454965.506&plusmn;0.000864 (5) |
| `pl_trandur` | `float64` | 22,722 non-null; min -0.068; median 3.37298275; max 53.6; 11,942 unique |
| `pl_trandurerr1` | `float64` | 18,129 non-null; min 0.0; median 0.0913; max 5.9; 2,849 unique |
| `pl_trandurerr2` | `float64` | 18,128 non-null; min -5.9; median -0.091; max 0.0; 2,839 unique |
| `pl_trandurlim` | `float64` | 25,458 non-null; min 0.0; median 0.0; max 1.0; 2 unique |
| `pl_trandurstr` | `object` | 14,831 unique incl. NA; top: None (17,433), 3.786&plusmn;0.18 (7), 3.401&plusmn;0.197 (5) |
| `sy_kmagstr` | `object` | 4,418 unique incl. NA; top: None (865), 12.18&plusmn;0.02 (103), 12.253&plusmn;0.020 (95) |
| `sy_umag` | `float64` | 4,120 non-null; min 12.4423; median 15.8639; max 25.2291; 575 unique |
| `sy_umagerr1` | `float64` | 4,120 non-null; min 0.0027536; median 0.0073994; max 8.54008; 577 unique |
| `sy_umagerr2` | `float64` | 4,120 non-null; min -8.54008; median -0.0073994; max -0.0027536; 577 unique |
| `sy_umagstr` | `object` | 580 unique incl. NA; top: None (36,035), 19.885200&plusmn;0.042516 (62), 15.1360000&plusmn;0.0094116 (56) |
| `sy_rmag` | `float64` | 4,120 non-null; min 8.46313; median 13.8071; max 17.9963; 575 unique |
| `sy_rmagerr1` | `float64` | 4,120 non-null; min 0.0001516; median 0.0030395; max 0.0149058; 576 unique |
| `sy_rmagerr2` | `float64` | 4,120 non-null; min -0.0149058; median -0.0030395; max -0.0001516; 576 unique |
| `sy_rmagstr` | `object` | 580 unique incl. NA; top: None (36,035), 15.9719000&plusmn;0.0039174 (62), 13.0020000&plusmn;0.0021332 (56) |
| `sy_imag` | `float64` | 4,122 non-null; min 7.75055; median 13.7711; max 22.73; 580 unique |
| `sy_imagerr1` | `float64` | 4,122 non-null; min 0.0001229; median 0.0033304; max 1.45; 576 unique |
| `sy_imagerr2` | `float64` | 4,122 non-null; min -1.48; median -0.0033304; max -0.0001229; 576 unique |
| `sy_imagstr` | `object` | 582 unique incl. NA; top: None (36,033), 15.4016000&plusmn;0.0040805 (62), 12.9854000&plusmn;0.0038095 (56) |
| `sy_zmag` | `float64` | 4,120 non-null; min 7.15757; median 13.4571; max 17.0259; 573 unique |
| `sy_zmagerr1` | `float64` | 4,120 non-null; min 0.0002994; median 0.0047055; max 0.0291883; 576 unique |
| `sy_zmagerr2` | `float64` | 4,120 non-null; min -0.0291883; median -0.0047055; max -0.0002994; 576 unique |
| `sy_zmagstr` | `object` | 580 unique incl. NA; top: None (36,035), 15.1016000&plusmn;0.0049271 (62), 14.5675000&plusmn;0.0235232 (56) |
| `sy_w1mag` | `float64` | 37,111 non-null; min -2.104; median 12.188; max 15.881; 3,230 unique |
| `sy_w1magerr1` | `float64` | 37,014 non-null; min 0.014; median 0.023; max 0.538; 240 unique |
| `sy_w1magerr2` | `float64` | 37,014 non-null; min -0.538; median -0.023; max -0.014; 240 unique |
| `sy_w1magstr` | `object` | 3,713 unique incl. NA; top: None (3,044), 12.053&plusmn;0.022 (103), 12.208&plusmn;0.024 (95) |
| `sy_w2mag` | `float64` | 37,112 non-null; min -1.241; median 12.231; max 16.218; 3,230 unique |
| `sy_w2magerr1` | `float64` | 37,031 non-null; min 0.009; median 0.023; max 0.494; 159 unique |
| `sy_w2magerr2` | `float64` | 37,031 non-null; min -0.494; median -0.023; max -0.009; 159 unique |
| `sy_w2magstr` | `object` | 3,818 unique incl. NA; top: None (3,043), 12.125&plusmn;0.022 (103), 12.254&plusmn;0.023 (95) |
| `sy_w3mag` | `float64` | 37,110 non-null; min -2.783; median 12.109; max 13.444; 2,997 unique |
| `sy_w3magerr1` | `float64` | 27,536 non-null; min 0.007; median 0.147; max 0.542; 504 unique |
| `sy_w3magerr2` | `float64` | 27,536 non-null; min -0.542; median -0.147; max -0.007; 504 unique |
| `sy_w3magstr` | `object` | 3,841 unique incl. NA; top: None (3,045), 12.119&plusmn;0.191 (103), 12.006&plusmn;0.222 (95) |
| `sy_w4mag` | `float64` | 37,107 non-null; min -3.227; median 9.168; max 10.081; 2,035 unique |
| `sy_w4magerr1` | `float64` | 6,133 non-null; min 0.001; median 0.21; max 0.542; 429 unique |
| `sy_w4magerr2` | `float64` | 6,133 non-null; min -0.542; median -0.21; max -0.001; 429 unique |
| `sy_w4magstr` | `object` | 2,411 unique incl. NA; top: None (3,048), 9.39 (172), 9.256 (172) |
| `sy_gmag` | `float64` | 4,120 non-null; min 9.91288; median 14.6927; max 19.6235; 577 unique |
| `sy_gmagerr1` | `float64` | 4,120 non-null; min 0.000204; median 0.0032079; max 0.0287515; 577 unique |
| `sy_gmagerr2` | `float64` | 4,120 non-null; min -0.0287515; median -0.0032079; max -0.000204; 577 unique |
| `sy_gmagstr` | `object` | 580 unique incl. NA; top: None (36,035), 17.2989000&plusmn;0.0046179 (62), 15.8159000&plusmn;0.0188418 (56) |
| `sy_gaiamag` | `float64` | 38,991 non-null; min 2.36431; median 13.9169; max 20.1861; 4,326 unique |
| `sy_gaiamagerr1` | `float64` | 38,991 non-null; min 0.000112; median 0.000353; max 0.063232; 1,138 unique |
| `sy_gaiamagerr2` | `float64` | 38,991 non-null; min -0.063232; median -0.000353; max -0.000112; 1,138 unique |
| `sy_gaiamagstr` | `object` | 4,436 unique incl. NA; top: None (1,164), 13.706200&plusmn;0.000271 (103), 14.755500&plusmn;0.000492 (95) |
| `sy_tmag` | `float64` | 39,297 non-null; min -1.2; median 13.4066; max 19.506; 4,368 unique |
| `sy_tmagerr1` | `float64` | 39,286 non-null; min 0.006; median 0.0068; max 2.6312; 595 unique |
| `sy_tmagerr2` | `float64` | 39,286 non-null; min -2.6312; median -0.0068; max -0.006; 595 unique |
| `sy_tmagstr` | `object` | 4,473 unique incl. NA; top: None (858), 13.2366&plusmn;0.0167 (103), 14.0239&plusmn;0.0062 (95) |
| `pl_controv_flag` | `int64` | 40,155 non-null; min 0; median 0.0; max 1; 2 unique |
| `pl_tsystemref` | `object` | 14 unique incl. NA; top: BJD (26,075), None (8,099), JD (3,020) |
| `st_metratio` | `object` | 4 unique incl. NA; top: [Fe/H] (20,912), None (15,232), [M/H] (3,991) |
| `st_spectype` | `object` | 314 unique incl. NA; top: None (36,985), G5 V (94), G0 V (89) |
| `sy_kepmag` | `float64` | 31,296 non-null; min 5.973; median 14.412; max 17.475; 1,898 unique |
| `sy_kepmagerr1` | `float64` |  |
| `sy_kepmagerr2` | `float64` |  |
| `sy_kepmagstr` | `float64` | 31,296 non-null; min 5.973; median 14.412; max 17.475; 1,898 unique |
| `st_rotp` | `float64` | 1,176 non-null; min 0.367; median 23.2; max 7900.0; 524 unique |
| `st_rotperr1` | `float64` | 979 non-null; min 4e-05; median 1.0; max 2477.0; 216 unique |
| `st_rotperr2` | `float64` | 979 non-null; min -2477.0; median -1.0; max -4e-05; 213 unique |
| `st_rotplim` | `float64` | 1,176 non-null; min -1.0; median 0.0; max 1.0; 3 unique |
| `st_rotpstr` | `object` | 666 unique incl. NA; top: None (38,979), 5.1&plusmn;0.1 (8), 9.754&plusmn;0.038 (7) |
| `pl_projobliq` | `float64` | 281 non-null; min -257.8; median 3.0; max 341.0; 213 unique |
| `pl_projobliqerr1` | `float64` | 279 non-null; min 0.12; median 8.7; max 100.0; 133 unique |
| `pl_projobliqerr2` | `float64` | 279 non-null; min -64.0; median -9.0; max -0.14; 137 unique |
| `pl_projobliqlim` | `float64` | 281 non-null; min 0.0; median 0.0; max 1.0; 2 unique |
| `pl_projobliqstr` | `object` | 279 unique incl. NA; top: None (39,874), 4.0&plusmn;10.0 (3), -36&plusmn;11 (2) |
| `x` | `float64` | 40,155 non-null; min -0.9993904824519724; median 0.2476322301448154; max 0.9980826461707332; 4,786 unique |
| `y` | `float64` | 40,155 non-null; min -0.9999763351046952; median -0.6491753293735604; max 0.9998861746277744; 4,786 unique |
| `z` | `float64` | 40,155 non-null; min -0.9999574607542904; median 0.6752725557465576; max 0.9997914676231742; 4,784 unique |
| `htm20` | `int64` | 40,155 non-null; min -2146451210; median -26221734.0; max 2147323689; 4,777 unique |
| `pl_rvamp` | `float64` | 5,041 non-null; min -404.0; median 36.6; max 10500.0; 2,795 unique |
| `pl_rvamperr1` | `float64` | 4,908 non-null; min 0.0; median 1.6; max 1100.0; 787 unique |
| `pl_rvamperr2` | `float64` | 4,908 non-null; min -1100.0; median -1.6; max 0.0; 782 unique |
| `pl_rvamplim` | `float64` | 5,041 non-null; min -1.0; median 0.0; max 1.0; 3 unique |
| `pl_rvampstr` | `object` | 4,649 unique incl. NA; top: None (35,114), 181.3&plusmn;2.6 (6), 89.1&plusmn;2.0 (5) |
| `pl_radj` | `float64` | 27,672 non-null; min 0.02408783; median 0.20608475; max 382.10254033; 7,969 unique |
| `pl_radjerr1` | `float64` | 26,924 non-null; min 0.0; median 0.032421685; max 791.52074226; 3,748 unique |
| `pl_radjerr2` | `float64` | 26,924 non-null; min -170.96050491; median -0.01962712; max 0.0; 3,552 unique |
| `pl_radjlim` | `float64` | 27,672 non-null; min -1.0; median 0.0; max 1.0; 3 unique |
| `pl_radjstr` | `object` | 20,857 unique incl. NA; top: None (12,483), <div><span class=supersubNumber">0… (14), <div><span class=supersubNumber">0… (14) |
| `pl_rade` | `float64` | 27,672 non-null; min 0.27; median 2.31; max 4282.98; 6,890 unique |
| `pl_radeerr1` | `float64` | 26,924 non-null; min 0.0; median 0.36391399999999996; max 8872.156; 3,358 unique |
| `pl_radeerr2` | `float64` | 26,924 non-null; min -1916.293; median -0.22; max 0.0; 3,201 unique |
| `pl_radelim` | `float64` | 30,419 non-null; min -1.0; median 0.0; max 1.0; 3 unique |
| `pl_radestr` | `object` | 20,979 unique incl. NA; top: None (12,483), 2.2&plusmn;1.1 (14), 2.4&plusmn;1.1 (14) |
| `pl_ratror` | `float64` | 21,866 non-null; min 0.003223; median 0.023112; max 62.554085; 8,389 unique |
| `pl_ratrorerr1` | `float64` | 21,540 non-null; min 0.0; median 0.00073; max 73.138474; 2,865 unique |
| `pl_ratrorerr2` | `float64` | 21,540 non-null; min -28.824688; median -0.000754; max 0.0; 2,946 unique |
| `pl_ratrorlim` | `float64` | 24,613 non-null; min 0.0; median 0.0; max 0.0; 1 unique |
| `pl_ratrorstr` | `object` | 13,778 unique incl. NA; top: None (18,289), 0.025&plusmn;0.012 (6), <div><span class=supersubNumber">0… (4) |
| `pl_ratdor` | `float64` | 17,529 non-null; min 0.838; median 18.53; max 1334.0; 5,509 unique |
| `pl_trueobliq` | `float64` | 77 non-null; min -4.0; median 35.6; max 158.0; 68 unique |
| `pl_trueobliqerr1` | `float64` | 70 non-null; min 0.95; median 10.15; max 60.0; 48 unique |
| `pl_trueobliqerr2` | `float64` | 70 non-null; min -60.0; median -9.7; max -0.97; 50 unique |
| `pl_trueobliqlim` | `float64` | 77 non-null; min -1.0; median 0.0; max 1.0; 3 unique |
| `pl_trueobliqstr` | `object` | 78 unique incl. NA; top: None (40,078), <div><span class=supersubNumber">2… (1), <div><span class=supersubNumber">8… (1) |
| `sy_icmag` | `float64` | 45 non-null; min 17.13; median 21.39; max 37.24; 26 unique |
| `sy_icmagerr1` | `float64` | 40 non-null; min 0.01; median 0.94; max 20.9; 22 unique |
| `sy_icmagerr2` | `float64` | 40 non-null; min -24.77; median -0.9299999999999999; max -0.01; 23 unique |
| `sy_icmagstr` | `object` | 27 unique incl. NA; top: None (40,110), 17.13&plusmn;0.01 (6), <div><span class=supersubNumber">2… (6) |
| `rowupdate` | `object` | 540 unique incl. NA; top: 2018-09-25 (2,844), 2014-11-21 (2,723), 2017-05-08 (2,719) |
| `pl_pubdate` | `object` | 312 unique incl. NA; top: 2018-08-16 (2,736), 2014-12-18 (2,723), 2017-08-31 00:00 (2,719) |
| `st_refname` | `object` | 2,482 unique incl. NA; top: <a refstr=STASSUN_ET_AL__2019 href… (7,402), <a refstr=Q1_Q17_DR25_KOI_TABLE hr… (3,088), <a refstr=Q1_Q16_KOI_TABLE href=ht… (2,720) |
| `releasedate` | `object` | 510 unique incl. NA; top: 2018-09-25 (2,736), 2014-11-21 (2,723), 2017-05-08 (2,719) |
| `dkin_flag` | `int64` | 40,155 non-null; min 0; median 0.0; max 1; 2 unique |
| `pl_ratdorerr1` | `float64` | 17,433 non-null; min 0.0; median 2.82; max 220.0; 1,946 unique |
| `pl_ratdorerr2` | `float64` | 17,433 non-null; min -184.0; median -3.0; max 0.0; 1,993 unique |
| `pl_ratdorlim` | `float64` | 20,274 non-null; min -1.0; median 0.0; max 0.0; 2 unique |
| `pl_ratdorstr` | `object` | 11,377 unique incl. NA; top: None (22,626), 25&plusmn;12 (15), 27&plusmn;13 (15) |
| `pl_imppar` | `float64` | 17,561 non-null; min -0.941; median 0.37; max 310.0; 3,523 unique |
| `pl_impparerr1` | `float64` | 17,290 non-null; min 0.0; median 0.1865795; max 140.0; 2,610 unique |
| `pl_impparerr2` | `float64` | 17,290 non-null; min -200.0; median -0.20335; max 0.0; 2,959 unique |
| `pl_impparlim` | `float64` | 20,306 non-null; min -1.0; median 0.0; max 1.0; 3 unique |
| `pl_impparstr` | `object` | 10,684 unique incl. NA; top: None (22,594), 0 (23), 0.5 (18) |
| `pl_cmassj` | `float64` | 88 non-null; min 0.00091285; median 0.7584592; max 12.02930278; 88 unique |
| `pl_cmassjerr1` | `float64` | 84 non-null; min 0.00053512; median 0.042000510000000005; max 5.24474381; 82 unique |
| `pl_cmassjerr2` | `float64` | 84 non-null; min -5.24474381; median -0.042000510000000005; max -0.00053512; 82 unique |
| `pl_cmassjlim` | `float64` | 88 non-null; min 0.0; median 0.0; max 0.0; 1 unique |
| `pl_cmassjstr` | `object` | 89 unique incl. NA; top: None (40,067), 0.121&plusmn;0.019 (1), 0.110&plusmn;0.018 (1) |
| `pl_cmasse` | `float64` | 88 non-null; min 0.29013072; median 241.06108756; max 3823.27330161; 88 unique |
| `pl_cmasseerr1` | `float64` | 84 non-null; min 0.17007663; median 13.492421985; max 1666.93692461; 82 unique |
| `pl_cmasseerr2` | `float64` | 84 non-null; min -1666.93692461; median -13.492421985; max -0.17007663; 82 unique |
| `pl_cmasselim` | `float64` | 88 non-null; min 0.0; median 0.0; max 0.0; 1 unique |
| `pl_cmassestr` | `object` | 89 unique incl. NA; top: None (40,067), 38.5&plusmn;6.0 (1), 35.0&plusmn;5.7 (1) |
| `pl_massj` | `float64` | 5,160 non-null; min 5.663e-05; median 0.489; max 290.0; 2,818 unique |
| `pl_massjerr1` | `float64` | 4,696 non-null; min 6.29e-06; median 0.053; max 58.0; 1,192 unique |
| `pl_massjerr2` | `float64` | 4,696 non-null; min -40.0; median -0.049; max -6.29e-06; 1,126 unique |
| `pl_massjlim` | `float64` | 5,192 non-null; min -1.0; median 0.0; max 1.0; 3 unique |
| `pl_massjstr` | `object` | 4,736 unique incl. NA; top: None (34,995), 0.066&plusmn;0.006 (16), <div><span class=supersubNumber">0… (8) |
| `pl_masse` | `float64` | 5,160 non-null; min 0.018; median 155.41848051; max 92170.23803; 3,249 unique |
| `pl_masseerr1` | `float64` | 4,696 non-null; min 0.002; median 17.0; max 18434.047606; 1,499 unique |
| `pl_masseerr2` | `float64` | 4,696 non-null; min -12713.13628; median -15.649999999999999; max -0.002; 1,407 unique |
| `pl_masselim` | `float64` | 5,192 non-null; min -1.0; median 0.0; max 1.0; 3 unique |
| `pl_massestr` | `object` | 4,864 unique incl. NA; top: None (34,995), 21&plusmn;2 (16), <div><span class=supersubNumber">1… (8) |
| `pl_bmassj` | `float64` | 7,614 non-null; min 4.72e-05; median 0.592; max 290.0; 3,782 unique |
| `pl_bmassjerr1` | `float64` | 6,912 non-null; min 0.0; median 0.053; max 78.55; 1,516 unique |
| `pl_bmassjerr2` | `float64` | 6,912 non-null; min -78.55; median -0.05; max 0.0; 1,436 unique |
| `pl_bmassjlim` | `float64` | 7,614 non-null; min -1.0; median 0.0; max 1.0; 3 unique |
| `pl_bmassjstr` | `object` | 6,974 unique incl. NA; top: None (32,541), 0.066&plusmn;0.006 (16), <div><span class=supersubNumber">0… (8) |
| `pl_bmasse` | `float64` | 7,615 non-null; min 0.015; median 188.15536; max 92170.23803; 4,622 unique |
| `pl_bmasseerr1` | `float64` | 6,918 non-null; min 0.0; median 16.84499; max 24965.5465; 1,947 unique |
| `pl_bmasseerr2` | `float64` | 6,918 non-null; min -24965.5465; median -15.8915; max 0.0; 1,853 unique |
| `pl_bmasselim` | `float64` | 7,615 non-null; min -1.0; median 0.0; max 1.0; 3 unique |
| `pl_bmassestr` | `object` | 7,208 unique incl. NA; top: None (32,540), 21&plusmn;2 (16), <div><span class=supersubNumber">1… (8) |
| `pl_bmassprov` | `object` | 4 unique incl. NA; top: None (32,540), Mass (5,160), Msini (2,427) |
| `pl_msinij` | `float64` | 2,741 non-null; min 4.72e-05; median 1.018; max 55.59; 1,819 unique |
| `pl_msinijerr1` | `float64` | 2,464 non-null; min 0.0; median 0.06; max 78.55; 773 unique |
| `pl_msinijerr2` | `float64` | 2,464 non-null; min -78.55; median -0.06; max 0.0; 771 unique |
| `pl_msinijlim` | `float64` | 2,741 non-null; min -1.0; median 0.0; max 1.0; 3 unique |
| `pl_msinijstr` | `object` | 2,612 unique incl. NA; top: None (37,414), 0.013&plusmn;0.002 (5), 0.02&plusmn;0.01 (4) |
| `pl_msinie` | `float64` | 2,743 non-null; min 0.015; median 323.537; max 17668.1697; 2,225 unique |
| `pl_msinieerr1` | `float64` | 2,471 non-null; min 0.0; median 19.06970442; max 24965.5465; 1,041 unique |
| `pl_msinieerr2` | `float64` | 2,471 non-null; min -24965.5465; median -19.069; max 0.0; 1,037 unique |
| `pl_msinielim` | `float64` | 2,743 non-null; min -1.0; median 0.0; max 1.0; 3 unique |
| `pl_msiniestr` | `object` | 2,673 unique incl. NA; top: None (37,412), 6&plusmn;3 (4), 108&plusmn;6 (3) |
| `st_teff` | `float64` | 36,499 non-null; min 415.0; median 5610.0; max 57000.0; 4,686 unique |
| `st_tefferr1` | `float64` | 35,542 non-null; min 0.0; median 113.0; max 6064.9; 3,407 unique |
| `st_tefferr2` | `float64` | 35,282 non-null; min -6064.9; median -117.0; max 0.0; 3,465 unique |
| `st_tefflim` | `float64` | 36,499 non-null; min 0.0; median 0.0; max 1.0; 2 unique |
| `st_teffstr` | `object` | 18,618 unique incl. NA; top: None (3,656), 6400&plusmn;100 (33), 5820.0&plusmn;25.0 (23) |
| `st_met` | `float64` | 25,120 non-null; min -2.5; median 0.0; max 7.79; 1,249 unique |
| `st_meterr1` | `float64` | 24,440 non-null; min 0.0; median 0.12; max 0.96; 500 unique |
| `st_meterr2` | `float64` | 24,440 non-null; min -1.0; median -0.14; max 0.0; 526 unique |
| `st_metlim` | `float64` | 27,433 non-null; min -1.0; median 0.0; max 1.0; 3 unique |
| `st_metstr` | `object` | 6,049 unique incl. NA; top: None (15,035), 0.16&plusmn;0.15 (240), 0.14&plusmn;0.15 (195) |
| `st_radv` | `float64` | 1,861 non-null; min -118.0; median -0.0157; max 129.75; 995 unique |
| `st_radverr1` | `float64` | 1,820 non-null; min 0.0; median 0.01; max 31.0; 266 unique |
| `st_radverr2` | `float64` | 1,679 non-null; min -31.0; median -0.012; max 0.0; 264 unique |
| `st_radvlim` | `float64` | 1,861 non-null; min 0.0; median 0.0; max 1.0; 2 unique |
| `st_radvstr` | `object` | 1,016 unique incl. NA; top: None (38,294), -9.5&plusmn;0.2 (11), 14.1&plusmn;0.3 (8) |
| `st_vsin` | `float64` | 3,560 non-null; min 0.0; median 2.9; max 299.0; 584 unique |
| `st_vsinerr1` | `float64` | 2,741 non-null; min 0.0; median 0.5; max 13.1; 159 unique |
| `st_vsinerr2` | `float64` | 2,553 non-null; min -21.1; median -0.5; max 0.0; 159 unique |
| `st_vsinlim` | `float64` | 3,560 non-null; min -1.0; median 0.0; max 1.0; 3 unique |
| `st_vsinstr` | `object` | 1,389 unique incl. NA; top: None (36,595), &lt;2 (201), &lt;2.0 (64) |
| `st_lum` | `float64` | 9,869 non-null; min -4.66; median -0.08619; max 3.26076; 3,598 unique |
| `st_lumerr1` | `float64` | 4,951 non-null; min 0.00017; median 0.02311; max 0.75; 1,697 unique |
| `st_lumerr2` | `float64` | 4,896 non-null; min -1.43136; median -0.02256; max -0.00017; 1,700 unique |
| `st_lumlim` | `float64` | 9,869 non-null; min 0.0; median 0.0; max 1.0; 2 unique |
| `st_lumstr` | `object` | 3,830 unique incl. NA; top: None (30,287), <div><span class=supersubNumber">-… (25), 0.1202010 (23) |
| `st_logg` | `float64` | 31,112 non-null; min 0.1; median 4.46649; max 8.07; 4,146 unique |
| `st_loggerr1` | `float64` | 25,641 non-null; min 0.0; median 0.068; max 2.01; 1,732 unique |
| `st_loggerr2` | `float64` | 25,640 non-null; min -3.51; median -0.105; max 0.0; 1,854 unique |
| `st_logglim` | `float64` | 31,112 non-null; min -1.0; median 0.0; max 1.0; 3 unique |
| `st_loggstr` | `object` | 12,422 unique incl. NA; top: None (9,043), 4.510&plusmn;0.300 (77), 4.540&plusmn;0.300 (74) |
| `st_age` | `float64` | 9,898 non-null; min 0.0; median 4.0; max 16.8; 750 unique |
| `st_ageerr1` | `float64` | 9,439 non-null; min 0.0; median 2.0; max 26.0; 814 unique |
| `st_ageerr2` | `float64` | 9,439 non-null; min -18.0; median -1.78; max 0.0; 659 unique |
| `st_agelim` | `float64` | 21,282 non-null; min -1.0; median 0.0; max 1.0; 3 unique |
| `st_agestr` | `object` | 5,495 unique incl. NA; top: None (30,257), 13.9&plusmn;3.7 (38), &gt;1 (36) |
| `st_mass` | `float64` | 33,628 non-null; min 0.0031; median 0.958144; max 23.56; 1,964 unique |
| `st_masserr1` | `float64` | 28,175 non-null; min 0.0; median 0.072; max 97.1; 1,570 unique |
| `st_masserr2` | `float64` | 28,020 non-null; min -97.1; median -0.067; max 0.0; 1,527 unique |
| `st_masslim` | `float64` | 33,635 non-null; min -1.0; median 0.0; max 1.0; 3 unique |
| `st_massstr` | `object` | 15,092 unique incl. NA; top: None (6,527), 0.96 (212), 1.0 (204) |
| `st_dens` | `float64` | 22,674 non-null; min 0.0026; median 1.501719; max 351.59589; 8,958 unique |
| `st_denserr1` | `float64` | 17,967 non-null; min 0.0; median 0.25037; max 532.58002; 6,686 unique |
| `st_denserr2` | `float64` | 17,967 non-null; min -197.05077; median -0.24; max 0.0; 6,664 unique |
| `st_denslim` | `float64` | 24,989 non-null; min 0.0; median 0.0; max 0.0; 1 unique |
| `st_densstr` | `object` | 10,182 unique incl. NA; top: None (17,481), 1.0271487 (23), <div><span class=supersubNumber">1… (22) |
| `st_rad` | `float64` | 36,705 non-null; min 0.0121; median 0.95; max 88.475; 5,483 unique |
| `st_raderr1` | `float64` | 30,969 non-null; min 0.0; median 0.077137; max 104.528; 2,717 unique |
| `st_raderr2` | `float64` | 30,816 non-null; min -73.63; median -0.062; max 0.0; 2,488 unique |
| `st_radlim` | `float64` | 36,705 non-null; min 0.0; median 0.0; max 1.0; 2 unique |
| `st_radstr` | `object` | 18,801 unique incl. NA; top: None (3,450), 0.51&plusmn;0.06 (27), 0.94&plusmn;0.02 (24) |
| `ttv_flag` | `int64` | 40,155 non-null; min 0; median 0.0; max 1; 2 unique |
| `ptv_flag` | `int64` | 40,155 non-null; min 0; median 0.0; max 1; 2 unique |
| `tran_flag` | `int64` | 40,155 non-null; min 0; median 1.0; max 1; 2 unique |
| `rv_flag` | `int64` | 40,155 non-null; min 0; median 0.0; max 1; 2 unique |
| `ast_flag` | `int64` | 40,155 non-null; min 0; median 0.0; max 1; 2 unique |
| `obm_flag` | `int64` | 40,155 non-null; min 0; median 0.0; max 1; 2 unique |
| `micro_flag` | `int64` | 40,155 non-null; min 0; median 0.0; max 1; 2 unique |
| `etv_flag` | `int64` | 40,155 non-null; min 0; median 0.0; max 1; 2 unique |
| `ima_flag` | `int64` | 40,155 non-null; min 0; median 0.0; max 1; 2 unique |
| `pul_flag` | `int64` | 40,155 non-null; min 0; median 0.0; max 1; 2 unique |
| `soltype` | `object` | 9 unique incl. NA; top: Published Confirmed (20,608), Kepler Project Candidate (q1_q17_d… (2,736), Kepler Project Candidate (q1_q16_k… (2,723) |
| `sy_snum` | `int64` | 40,155 non-null; min 1; median 1.0; max 4; 4 unique |
| `sy_pnum` | `int64` | 40,155 non-null; min 1; median 1.0; max 8; 8 unique |
| `sy_mnum` | `int64` | 40,155 non-null; min 0; median 0.0; max 0; 1 unique |
| `cb_flag` | `int64` | 40,155 non-null; min 0; median 0.0; max 1; 2 unique |
| `st_nphot` | `int64` | 40,155 non-null; min 0; median 0.0; max 70; 35 unique |
| `st_nrvc` | `int64` | 40,155 non-null; min 0; median 0.0; max 12; 13 unique |
| `st_nspec` | `int64` | 40,155 non-null; min 0; median 0.0; max 13; 12 unique |
| `pl_nespec` | `int64` | 40,155 non-null; min 0; median 0.0; max 37; 23 unique |
| `pl_ntranspec` | `int64` | 40,155 non-null; min 0; median 0.0; max 33; 21 unique |
| `pl_ndispec` | `int64` | 40,155 non-null; min 0; median 0.0; max 10; 7 unique |
| `pl_nnotes` | `int64` | 40,155 non-null; min 0; median 1.0; max 16; 16 unique |
| `sy_pm` | `float64` | 39,169 non-null; min 0.1586386; median 12.4020818; max 10393.5508325; 4,459 unique |
| `sy_pmerr1` | `float64` | 39,169 non-null; min 0.0174922; median 0.0466322; max 8.0; 4,425 unique |
| `sy_pmerr2` | `float64` | 39,164 non-null; min -8.0; median -0.0466248; max -0.0174922; 4,422 unique |
| `sy_pmstr` | `object` | 4,460 unique incl. NA; top: None (986), 7.0692817&plusmn;0.0287745 (103), 7.3158320&plusmn;0.0456227 (95) |
| `sy_pmra` | `float64` | 39,169 non-null; min -3781.31; median -0.976046; max 6767.26; 4,455 unique |
| `sy_pmraerr1` | `float64` | 39,169 non-null; min 0.0148952; median 0.045562; max 8.0; 4,406 unique |
| `sy_pmraerr2` | `float64` | 39,164 non-null; min -8.0; median -0.04553765; max -0.0148952; 4,404 unique |
| `sy_pmrastr` | `object` | 4,460 unique incl. NA; top: None (986), -0.0379221&plusmn;0.0253491 (103), -1.3796200&plusmn;0.0365041 (95) |
| `sy_pmdec` | `float64` | 39,169 non-null; min -5709.22; median -5.17822; max 10362.5; 4,454 unique |
| `sy_pmdecerr1` | `float64` | 39,169 non-null; min 0.0172533; median 0.0461912; max 8.0; 4,418 unique |
| `sy_pmdecerr2` | `float64` | 39,164 non-null; min -8.0; median -0.0461912; max -0.0172533; 4,415 unique |
| `sy_pmdecstr` | `object` | 4,460 unique incl. NA; top: None (986), -7.0691800&plusmn;0.0287746 (103), -7.1845700&plusmn;0.0459243 (95) |
| `sy_plx` | `float64` | 37,679 non-null; min 0.251495; median 1.77633; max 768.5; 4,305 unique |
| `sy_plxerr1` | `float64` | 37,679 non-null; min 0.0117367; median 0.0253128; max 3.88; 4,296 unique |
| `sy_plxerr2` | `float64` | 37,679 non-null; min -3.88; median -0.0253128; max -0.0117367; 4,296 unique |
| `sy_plxstr` | `object` | 4,314 unique incl. NA; top: None (2,476), 1.5184100&plusmn;0.0151448 (103), 2.6780100&plusmn;0.0210459 (95) |
| `sy_dist` | `float64` | 39,299 non-null; min 1.30119; median 571.034; max 8980.0; 4,741 unique |
| `sy_disterr1` | `float64` | 38,435 non-null; min 0.00034; median 7.264; max 3160.0; 4,127 unique |
| `sy_disterr2` | `float64` | 38,435 non-null; min -2900.0; median -7.167; max 2700.0; 4,161 unique |
| `sy_diststr` | `object` | 4,974 unique incl. NA; top: None (856), 646.346&plusmn;6.375 (103), 369.4510&plusmn;2.8945 (95) |
| `sy_bmag` | `float64` | 38,614 non-null; min 0.011; median 14.881; max 21.084; 3,504 unique |
| `sy_bmagerr1` | `float64` | 38,609 non-null; min 0.0; median 0.061; max 1.054; 447 unique |
| `sy_bmagerr2` | `float64` | 38,609 non-null; min -1.054; median -0.061; max 0.0; 447 unique |
| `sy_bmagstr` | `object` | 4,337 unique incl. NA; top: None (1,541), 14.635&plusmn;0.030 (103), 16.303&plusmn;0.000 (95) |
| `sy_vmag` | `float64` | 39,292 non-null; min 0.872; median 14.1215; max 45.34; 3,338 unique |
| `sy_vmagerr1` | `float64` | 39,279 non-null; min 0.001; median 0.092; max 11.0; 200 unique |
| `sy_vmagerr2` | `float64` | 39,278 non-null; min -12.27; median -0.092; max -0.001; 199 unique |
| `sy_vmagstr` | `object` | 4,127 unique incl. NA; top: None (863), 13.817&plusmn;0.092 (103), 15.230&plusmn;0.172 (95) |
| `sy_jmag` | `float64` | 39,257 non-null; min -2.095; median 12.665; max 25.34; 3,492 unique |
| `sy_jmagerr1` | `float64` | 39,159 non-null; min 0.017; median 0.024; max 8.888; 119 unique |
| `sy_jmagerr2` | `float64` | 39,159 non-null; min -8.888; median -0.024; max -0.017; 119 unique |
| `sy_jmagstr` | `object` | 4,335 unique incl. NA; top: None (898), 12.548&plusmn;0.024 (103), 12.954&plusmn;0.023 (95) |
| `sy_hmag` | `float64` | 39,288 non-null; min -2.775; median 12.283; max 33.83; 3,495 unique |
| `sy_hmagerr1` | `float64` | 39,150 non-null; min 0.014; median 0.025; max 6.99; 153 unique |
| `sy_hmagerr2` | `float64` | 39,150 non-null; min -8.99; median -0.025; max -0.014; 153 unique |
| `sy_hmagstr` | `object` | 4,414 unique incl. NA; top: None (867), 12.354&plusmn;0.022 (105), 12.237&plusmn;0.024 (103) |
| `sy_kmag` | `float64` | 39,290 non-null; min -3.044; median 12.204; max 35.33; 3,514 unique |
| `sy_kmagerr1` | `float64` | 39,048 non-null; min 0.011; median 0.024; max 9.995; 168 unique |
| `sy_kmagerr2` | `float64` | 39,048 non-null; min -11.14; median -0.024; max -0.011; 166 unique |

### Missingness hotspots

| Column | Missing | Missing % |
|---|---:|---:|
| `sy_kepmagerr1` | 40,155 | 100.00% |
| `sy_kepmagerr2` | 40,155 | 100.00% |
| `sy_icmagerr2` | 40,115 | 99.90% |
| `sy_icmagerr1` | 40,115 | 99.90% |
| `sy_icmagstr` | 40,110 | 99.89% |
| `sy_icmag` | 40,110 | 99.89% |
| `pl_occdeperr1` | 40,108 | 99.88% |
| `pl_occdeperr2` | 40,108 | 99.88% |
| `pl_occdep` | 40,105 | 99.88% |
| `pl_occdepstr` | 40,105 | 99.88% |
| `pl_occdeplim` | 40,105 | 99.88% |
| `pl_trueobliqerr1` | 40,085 | 99.83% |

### Date/time candidates

- `disc_pubdate`: 40,141 valid; 1992-01-01 00:00:00 to 2026-09-01 00:00:00 (datetime)
- `disc_year`: 40,155 valid; 1992 to 2026 (year)
- `rowupdate`: 40,154 valid; 2013-10-28 00:00:00 to 2026-09-11 00:00:00 (datetime)
- `pl_pubdate`: 24,282 valid; 1992-01-01 00:00:00 to 2026-09-01 00:00:00 (datetime)
- `releasedate`: 40,140 valid; 2013-10-28 00:00:00 to 2026-09-11 00:00:00 (datetime)

---

## Netflix TV Shows and Movies (titles + credits)

- Source: Kaggle: victorsoeiro/netflix-tv-shows-and-movies
- Local file: `data/processed/netflix/titles.csv`
- Shape: **5,850 rows × 15 columns**
- Size: 1.93 MB; duplicate rows: 0; missing cells: 9.31%

### Schema

| Column | Type | Non-null / unique or range |
|---|---|---|
| `id` | `object` | 5,850 unique incl. NA; top: ts300399 (1), tm912400 (1), ts89361 (1) |
| `title` | `object` | 5,799 unique incl. NA; top: The Gift (3), Connected (3), Fearless (2) |
| `type` | `object` | 2 unique incl. NA; top: MOVIE (3,744), SHOW (2,106) |
| `description` | `object` | 5,830 unique incl. NA; top: None (18), Five families struggle with the up… (2), Away from school, during the winte… (2) |
| `release_year` | `int64` | 5,850 non-null; min 1945; median 2018.0; max 2022; 63 unique |
| `age_certification` | `object` | 12 unique incl. NA; top: None (2,619), TV-MA (883), R (556) |
| `runtime` | `int64` | 5,850 non-null; min 0; median 83.0; max 240; 202 unique |
| `genres` | `object` | 1,726 unique incl. NA; top: ['comedy'] (484), ['documentation'] (329), ['drama'] (328) |
| `production_countries` | `object` | 452 unique incl. NA; top: ['US'] (1,959), ['IN'] (599), ['JP'] (264) |
| `seasons` | `float64` | 2,106 non-null; min 1.0; median 1.0; max 42.0; 26 unique |
| `imdb_id` | `object` | 5,448 unique incl. NA; top: None (403), tt12742136 (1), tt10628250 (1) |
| `imdb_score` | `float64` | 5,368 non-null; min 1.5; median 6.6; max 9.6; 80 unique |
| `imdb_votes` | `float64` | 5,352 non-null; min 5.0; median 2233.5; max 2294231.0; 3,880 unique |
| `tmdb_popularity` | `float64` | 5,759 non-null; min 0.0094417458789051; median 6.821; max 2274.044; 4,889 unique |
| `tmdb_score` | `float64` | 5,539 non-null; min 0.5; median 6.9; max 10.0; 394 unique |

### Missingness hotspots

| Column | Missing | Missing % |
|---|---:|---:|
| `seasons` | 3,744 | 64.00% |
| `age_certification` | 2,619 | 44.77% |
| `imdb_votes` | 498 | 8.51% |
| `imdb_score` | 482 | 8.24% |
| `imdb_id` | 403 | 6.89% |
| `tmdb_score` | 311 | 5.32% |
| `tmdb_popularity` | 91 | 1.56% |
| `description` | 18 | 0.31% |
| `title` | 1 | 0.02% |

### Date/time candidates

- `release_year`: 5,850 valid; 1945 to 2022 (year)

---

## Netflix TV Shows and Movies — credits table

- Source: Kaggle: victorsoeiro/netflix-tv-shows-and-movies
- Local file: `data/processed/netflix/credits.csv`
- Shape: **77,801 rows × 5 columns**
- Size: 3.64 MB; duplicate rows: 0; missing cells: 2.51%

### Schema

| Column | Type | Non-null / unique or range |
|---|---|---|
| `person_id` | `int64` | 77,801 non-null; min 7; median 198358.0; max 2462818; 54,589 unique |
| `id` | `object` | 5,489 unique incl. NA; top: tm32982 (208), tm244149 (174), tm39888 (161) |
| `name` | `object` | 54,314 unique incl. NA; top: Boman Irani (25), Kareena Kapoor Khan (25), Shah Rukh Khan (23) |
| `character` | `object` | 47,275 unique incl. NA; top: None (9,772), Self (1,950), Himself (1,276) |
| `role` | `object` | 2 unique incl. NA; top: ACTOR (73,251), DIRECTOR (4,550) |

### Missingness hotspots

| Column | Missing | Missing % |
|---|---:|---:|
| `character` | 9,772 | 12.56% |

---
