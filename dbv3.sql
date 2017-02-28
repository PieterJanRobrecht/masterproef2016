-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`test`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`test` (
  `idTest` INT(11) NOT NULL,
  `purpose` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idTest`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`diagnosecheck`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`diagnosecheck` (
  `idDiagnoseCheck` INT(11) NOT NULL AUTO_INCREMENT,
  `endResult` VARCHAR(45) NULL DEFAULT NULL,
  `startTime` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `endTime` DATETIME NULL DEFAULT NULL,
  `Test_idTest` INT(11) NOT NULL,
  PRIMARY KEY (`idDiagnoseCheck`),
  INDEX `fk_DiagnoseCheck_Test1_idx` (`Test_idTest` ASC),
  CONSTRAINT `fk_DiagnoseCheck_Test1`
    FOREIGN KEY (`Test_idTest`)
    REFERENCES `mydb`.`test` (`idTest`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`package`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`package` (
  `idPackage` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `version` VARCHAR(45) NOT NULL,
  `description` VARCHAR(45) NOT NULL,
  `type` VARCHAR(45) NULL DEFAULT NULL,
  `priority` INT(11) NOT NULL,
  `releaseDate` DATE NULL DEFAULT NULL,
  `optional` TINYINT(1) NOT NULL,
  `framework` TINYINT(1) NOT NULL,
  `location` VARCHAR(120) NULL DEFAULT NULL,
  PRIMARY KEY (`idPackage`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`installer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`installer` (
  `idInstaller` INT(11) NOT NULL AUTO_INCREMENT,
  `installerVersion` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `diskLocation` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idInstaller`))
ENGINE = InnoDB
AUTO_INCREMENT = 12
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`tower`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tower` (
  `idTower` INT(11) NOT NULL AUTO_INCREMENT,
  `Installer_idInstaller` INT(11) NULL DEFAULT NULL,
  `alias` VARCHAR(45) NOT NULL,
  `geolocation` VARCHAR(45) NOT NULL,
  `idInCompany` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `serialNumber` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idTower`),
  UNIQUE INDEX `alias_UNIQUE` (`alias` ASC),
  INDEX `fk_Toren_Installer1_idx` (`Installer_idInstaller` ASC),
  CONSTRAINT `fk_Toren_Installer1`
    FOREIGN KEY (`Installer_idInstaller`)
    REFERENCES `mydb`.`installer` (`idInstaller`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 10
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`hardware_component`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`hardware_component` (
  `idComponent` INT(11) NOT NULL AUTO_INCREMENT,
  `Tower_idTower` INT(11) NOT NULL,
  `calibrationNumber` VARCHAR(45) NOT NULL,
  `manufacturer` VARCHAR(45) NOT NULL,
  `productNumber` VARCHAR(45) NOT NULL,
  `serialNumber` VARCHAR(45) NOT NULL,
  `firmwareVersion` VARCHAR(45) NOT NULL,
  `Package_idPackage` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`idComponent`),
  INDEX `fk_Component_Toren1_idx` (`Tower_idTower` ASC),
  INDEX `fk_Component_Package1_idx` (`Package_idPackage` ASC),
  CONSTRAINT `fk_Component_Package1`
    FOREIGN KEY (`Package_idPackage`)
    REFERENCES `mydb`.`package` (`idPackage`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Component_Toren1`
    FOREIGN KEY (`Tower_idTower`)
    REFERENCES `mydb`.`tower` (`idTower`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`installer_has_diagnosecheck`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`installer_has_diagnosecheck` (
  `installer_idInstaller` INT(11) NOT NULL,
  `diagnosecheck_idDiagnoseCheck` INT(11) NOT NULL,
  PRIMARY KEY (`installer_idInstaller`, `diagnosecheck_idDiagnoseCheck`),
  INDEX `fk_installer_has_diagnosecheck_diagnosecheck1_idx` (`diagnosecheck_idDiagnoseCheck` ASC),
  INDEX `fk_installer_has_diagnosecheck_installer1_idx` (`installer_idInstaller` ASC),
  CONSTRAINT `fk_installer_has_diagnosecheck_diagnosecheck1`
    FOREIGN KEY (`diagnosecheck_idDiagnoseCheck`)
    REFERENCES `mydb`.`diagnosecheck` (`idDiagnoseCheck`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_installer_has_diagnosecheck_installer1`
    FOREIGN KEY (`installer_idInstaller`)
    REFERENCES `mydb`.`installer` (`idInstaller`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`installer_has_package`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`installer_has_package` (
  `Installer_idInstaller` INT(11) NOT NULL,
  `Package_idPackage` INT(11) NOT NULL,
  PRIMARY KEY (`Installer_idInstaller`, `Package_idPackage`),
  INDEX `fk_Installer_has_Package_Package1_idx` (`Package_idPackage` ASC),
  INDEX `fk_Installer_has_Package_Installer_idx` (`Installer_idInstaller` ASC),
  CONSTRAINT `fk_Installer_has_Package_Installer`
    FOREIGN KEY (`Installer_idInstaller`)
    REFERENCES `mydb`.`installer` (`idInstaller`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Installer_has_Package_Package1`
    FOREIGN KEY (`Package_idPackage`)
    REFERENCES `mydb`.`package` (`idPackage`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`package_depends_on_package`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`package_depends_on_package` (
  `package_idPackage` INT(11) NOT NULL,
  `package_idPackage1` INT(11) NOT NULL,
  PRIMARY KEY (`package_idPackage`, `package_idPackage1`),
  INDEX `fk_package_has_package_package2_idx` (`package_idPackage1` ASC),
  INDEX `fk_package_has_package_package1_idx` (`package_idPackage` ASC),
  CONSTRAINT `fk_package_has_package_package1`
    FOREIGN KEY (`package_idPackage`)
    REFERENCES `mydb`.`package` (`idPackage`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_package_has_package_package2`
    FOREIGN KEY (`package_idPackage1`)
    REFERENCES `mydb`.`package` (`idPackage`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`package_has_diagnosecheck`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`package_has_diagnosecheck` (
  `package_idPackage` INT(11) NOT NULL,
  `diagnosecheck_idDiagnoseCheck` INT(11) NOT NULL,
  PRIMARY KEY (`package_idPackage`, `diagnosecheck_idDiagnoseCheck`),
  INDEX `fk_package_has_diagnosecheck_diagnosecheck1_idx` (`diagnosecheck_idDiagnoseCheck` ASC),
  INDEX `fk_package_has_diagnosecheck_package1_idx` (`package_idPackage` ASC),
  CONSTRAINT `fk_package_has_diagnosecheck_diagnosecheck1`
    FOREIGN KEY (`diagnosecheck_idDiagnoseCheck`)
    REFERENCES `mydb`.`diagnosecheck` (`idDiagnoseCheck`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_package_has_diagnosecheck_package1`
    FOREIGN KEY (`package_idPackage`)
    REFERENCES `mydb`.`package` (`idPackage`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
