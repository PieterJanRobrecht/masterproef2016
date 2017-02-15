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
-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Installer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Installer` (
  `idInstaller` INT NOT NULL AUTO_INCREMENT,
  `installerVersion` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `diskLocation` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idInstaller`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Tower`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Tower` (
  `idTower` INT NOT NULL AUTO_INCREMENT,
  `Installer_idInstaller` INT NOT NULL,
  `alias` VARCHAR(45) NOT NULL,
  `geolocatie` VARCHAR(45) NOT NULL,
  `idInCompany` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `serialNumber` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idTower`),
  INDEX `fk_Toren_Installer1_idx` (`Installer_idInstaller` ASC),
  UNIQUE INDEX `alias_UNIQUE` (`alias` ASC),
  CONSTRAINT `fk_Toren_Installer1`
    FOREIGN KEY (`Installer_idInstaller`)
    REFERENCES `mydb`.`Installer` (`idInstaller`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Package`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Package` (
  `idPackage` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `version` VARCHAR(45) NOT NULL,
  `description` VARCHAR(45) NOT NULL,
  `type` VARCHAR(45) NULL,
  `priority` INT NOT NULL,
  `releaseDate` DATE NULL,
  PRIMARY KEY (`idPackage`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Component`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Component` (
  `idComponent` INT NOT NULL AUTO_INCREMENT,
  `Tower_idTower` INT NOT NULL,
  `calibrationNumber` INT NOT NULL,
  `manufacturer` VARCHAR(45) NOT NULL,
  `productNumber` VARCHAR(45) NOT NULL,
  `serialNumber` VARCHAR(45) NOT NULL,
  `firmwareVersion` VARCHAR(45) NOT NULL,
  `Package_idPackage` INT NOT NULL,
  PRIMARY KEY (`idComponent`),
  INDEX `fk_Component_Toren1_idx` (`Tower_idTower` ASC),
  INDEX `fk_Component_Package1_idx` (`Package_idPackage` ASC),
  CONSTRAINT `fk_Component_Toren1`
    FOREIGN KEY (`Tower_idTower`)
    REFERENCES `mydb`.`Tower` (`idTower`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Component_Package1`
    FOREIGN KEY (`Package_idPackage`)
    REFERENCES `mydb`.`Package` (`idPackage`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Test`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Test` (
  `idTest` INT NOT NULL,
  `purpose` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idTest`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`DiagnoseCheck`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`DiagnoseCheck` (
  `idDiagnoseCheck` INT NOT NULL AUTO_INCREMENT,
  `endResult` VARCHAR(45) NULL,
  `startTime` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `endTime` DATETIME NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `Test_idTest` INT NOT NULL,
  PRIMARY KEY (`idDiagnoseCheck`),
  INDEX `fk_DiagnoseCheck_Test1_idx` (`Test_idTest` ASC),
  CONSTRAINT `fk_DiagnoseCheck_Test1`
    FOREIGN KEY (`Test_idTest`)
    REFERENCES `mydb`.`Test` (`idTest`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Installer_has_Package`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Installer_has_Package` (
  `Installer_idInstaller` INT NOT NULL,
  `Package_idPackage` INT NOT NULL,
  PRIMARY KEY (`Installer_idInstaller`, `Package_idPackage`),
  INDEX `fk_Installer_has_Package_Package1_idx` (`Package_idPackage` ASC),
  INDEX `fk_Installer_has_Package_Installer_idx` (`Installer_idInstaller` ASC),
  CONSTRAINT `fk_Installer_has_Package_Installer`
    FOREIGN KEY (`Installer_idInstaller`)
    REFERENCES `mydb`.`Installer` (`idInstaller`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Installer_has_Package_Package1`
    FOREIGN KEY (`Package_idPackage`)
    REFERENCES `mydb`.`Package` (`idPackage`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Tower_has_DiagnoseCheck`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Tower_has_DiagnoseCheck` (
  `Tower_idTower` INT NOT NULL,
  `DiagnoseCheck_idDiagnoseCheck` INT NOT NULL,
  PRIMARY KEY (`Tower_idTower`, `DiagnoseCheck_idDiagnoseCheck`),
  INDEX `fk_Toren_has_DiagnoseCheck_DiagnoseCheck1_idx` (`DiagnoseCheck_idDiagnoseCheck` ASC),
  INDEX `fk_Toren_has_DiagnoseCheck_Toren1_idx` (`Tower_idTower` ASC),
  CONSTRAINT `fk_Toren_has_DiagnoseCheck_Toren1`
    FOREIGN KEY (`Tower_idTower`)
    REFERENCES `mydb`.`Tower` (`idTower`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Toren_has_DiagnoseCheck_DiagnoseCheck1`
    FOREIGN KEY (`DiagnoseCheck_idDiagnoseCheck`)
    REFERENCES `mydb`.`DiagnoseCheck` (`idDiagnoseCheck`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Component_has_DiagnoseCheck`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Component_has_DiagnoseCheck` (
  `Component_idComponent` INT NOT NULL,
  `DiagnoseCheck_idDiagnoseCheck` INT NOT NULL,
  PRIMARY KEY (`Component_idComponent`, `DiagnoseCheck_idDiagnoseCheck`),
  INDEX `fk_Component_has_DiagnoseCheck_DiagnoseCheck1_idx` (`DiagnoseCheck_idDiagnoseCheck` ASC),
  INDEX `fk_Component_has_DiagnoseCheck_Component1_idx` (`Component_idComponent` ASC),
  CONSTRAINT `fk_Component_has_DiagnoseCheck_Component1`
    FOREIGN KEY (`Component_idComponent`)
    REFERENCES `mydb`.`Component` (`idComponent`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Component_has_DiagnoseCheck_DiagnoseCheck1`
    FOREIGN KEY (`DiagnoseCheck_idDiagnoseCheck`)
    REFERENCES `mydb`.`DiagnoseCheck` (`idDiagnoseCheck`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`installer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`installer` (
  `idInstaller` INT(11) NOT NULL AUTO_INCREMENT,
  `installerVersionNumber` VARCHAR(45) NOT NULL,
  `diskLocation` VARCHAR(120) NOT NULL,
  `installerName` VARCHAR(45) NULL DEFAULT NULL,
  `executableLocation` VARCHAR(120) NULL DEFAULT NULL,
  PRIMARY KEY (`idInstaller`))
ENGINE = InnoDB
AUTO_INCREMENT = 54
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`client`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`client` (
  `idClient` INT(11) NOT NULL AUTO_INCREMENT,
  `clientUUID` VARCHAR(45) NOT NULL,
  `Installer_idInstaller` INT(11) NULL DEFAULT NULL,
  `status` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`idClient`),
  INDEX `fk_Server_Version_idx` (`Installer_idInstaller` ASC),
  CONSTRAINT `fk_Server_Version`
    FOREIGN KEY (`Installer_idInstaller`)
    REFERENCES `mydb`.`installer` (`idInstaller`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 28
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`package`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`package` (
  `idModule` INT(11) NOT NULL AUTO_INCREMENT,
  `packageVersionNumber` VARCHAR(45) NOT NULL,
  `packageName` VARCHAR(45) NOT NULL,
  `diskLocation` VARCHAR(120) NOT NULL,
  `priority` INT(11) NULL DEFAULT NULL,
  `description` VARCHAR(120) NULL DEFAULT NULL,
  `releaseDate` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`idModule`))
ENGINE = InnoDB
AUTO_INCREMENT = 57
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`installer_has_package`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`installer_has_package` (
  `Installer_idInstaller` INT(11) NOT NULL,
  `Package_idPackage` INT(11) NOT NULL,
  PRIMARY KEY (`Installer_idInstaller`, `Package_idPackage`),
  INDEX `fk_Version_has_Module_Module1_idx` (`Package_idPackage` ASC),
  INDEX `fk_Version_has_Module_Version1_idx` (`Installer_idInstaller` ASC),
  CONSTRAINT `fk_Version_has_Module_Module1`
    FOREIGN KEY (`Package_idPackage`)
    REFERENCES `mydb`.`package` (`idModule`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Version_has_Module_Version1`
    FOREIGN KEY (`Installer_idInstaller`)
    REFERENCES `mydb`.`installer` (`idInstaller`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
