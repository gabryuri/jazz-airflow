CREATE TABLE crawling.crawled_matches (
                    match_id int,
                    description text,
                    demo_id int,
                    match_played_at timestamp,                    
                    created_at timestamp,
                    updated_at timestamp,
                    last_seen_at timestamp, 
                    PRIMARY KEY (match_id) )