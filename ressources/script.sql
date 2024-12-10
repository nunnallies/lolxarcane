CREATE TABLE `lolarcane`.`match` ( `matchId` VARCHAR(200) NOT NULL , 
                                   `gameMode` VARCHAR(50) NOT NULL , 
                                   `gameType` INT NOT NULL , 
                                   `gameStartDate` DATE NOT NULL ,
                                   `gameDuration` INT NOT NULL , 
                                   `summonnersPuuid` LONGTEXT NOT NULL , 
                                   `championList` LONGTEXT NOT NULL , 
                                   PRIMARY KEY (`matchId`)
                                   ) 

CREATE TABLE `lolarcane`.`players` ( `puuid` TEXT NOT NULL , 
                                     `Rank` VARCHAR(50) NOT NULL , 
                                     `division` INT NOT NULL , 
                                     PRIMARY KEY (`puuid`(200))
                                     )
                                     
CREATE TABLE `lolarcane`.`champion` ( `championId` INT NOT NULL AUTO_INCREMENT , 
                                      `name` INT NOT NULL , 
                                      `pickrate` FLOAT NOT NULL , 
                                      PRIMARY KEY (`championId`)
                                      )

ALTER TABLE `players` ADD `summonerId` VARCHAR(60) NOT NULL AFTER `puuid`

