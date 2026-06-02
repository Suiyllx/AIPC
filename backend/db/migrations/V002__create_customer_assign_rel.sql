-- ============================================================
-- 客户分配关系表 DDL
-- 版本: V002
-- 说明: 记录客户当前的归属关系（每客户至多一条）
--       ASSIGN_SOURCE=0: 数仓每日同步自 T_DDW_F22_LCSC_CUST_RLN
--       ASSIGN_SOURCE=1: 平台手动分配，可撤回
-- ============================================================


-- ------------------------------------------------------------
-- 1. 主表
-- ------------------------------------------------------------
CREATE TABLE custgroup.T_CUSTOMER_ASSIGN_REL
(
    ID             NUMBER         NOT NULL,           -- 主键
    CLIENT_ID      VARCHAR2(20)   NOT NULL,           -- 客户资金账号
    BRANCH_NO      VARCHAR2(10)   NOT NULL,           -- 营业部编号
    LOGIN_ID       VARCHAR2(20)   NOT NULL,           -- 归属员工OA
    EMP_NAME       VARCHAR2(50),                      -- 归属员工姓名
    ASSIGN_TIME    TIMESTAMP      NOT NULL,           -- 关系建立时间
    LOGIN_ID_OP    VARCHAR2(20),                      -- 分配操作人OA（外部导入时为空）
    EMP_NM_OP      VARCHAR2(50),                      -- 分配操作人姓名（外部导入时为空）
    ASSIGN_SOURCE  NUMBER(1)      DEFAULT 1 NOT NULL, -- 0: 外部导入, 1: 手动分配
    UPDATE_TIME    TIMESTAMP      DEFAULT LOCALTIMESTAMP, -- 记录最后更新时间
    CONSTRAINT PK_CUST_ASSIGN_REL PRIMARY KEY (ID),
    CONSTRAINT UQ_CUST_ASSIGN_REL_CLIENT UNIQUE (CLIENT_ID)  -- 每个客户只能有一条当前关系
);

COMMENT ON TABLE  custgroup.T_CUSTOMER_ASSIGN_REL                  IS '客户分配关系表，每客户至多一条';
COMMENT ON COLUMN custgroup.T_CUSTOMER_ASSIGN_REL.ID               IS '主键';
COMMENT ON COLUMN custgroup.T_CUSTOMER_ASSIGN_REL.CLIENT_ID        IS '客户资金账号';
COMMENT ON COLUMN custgroup.T_CUSTOMER_ASSIGN_REL.BRANCH_NO        IS '营业部编号';
COMMENT ON COLUMN custgroup.T_CUSTOMER_ASSIGN_REL.LOGIN_ID         IS '归属员工OA';
COMMENT ON COLUMN custgroup.T_CUSTOMER_ASSIGN_REL.EMP_NAME         IS '归属员工姓名';
COMMENT ON COLUMN custgroup.T_CUSTOMER_ASSIGN_REL.ASSIGN_TIME      IS '关系建立时间';
COMMENT ON COLUMN custgroup.T_CUSTOMER_ASSIGN_REL.LOGIN_ID_OP      IS '分配操作人OA，外部导入时为空';
COMMENT ON COLUMN custgroup.T_CUSTOMER_ASSIGN_REL.EMP_NM_OP        IS '分配操作人姓名，外部导入时为空';
COMMENT ON COLUMN custgroup.T_CUSTOMER_ASSIGN_REL.ASSIGN_SOURCE    IS '来源: 0=外部导入, 1=手动分配';
COMMENT ON COLUMN custgroup.T_CUSTOMER_ASSIGN_REL.UPDATE_TIME      IS '记录最后更新时间';


-- ------------------------------------------------------------
-- 2. 主键序列
-- ------------------------------------------------------------
CREATE SEQUENCE custgroup.SEQ_CUST_ASSIGN_REL
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;


-- ------------------------------------------------------------
-- 3. 触发器：INSERT 时自动填充 ID
-- ------------------------------------------------------------
CREATE OR REPLACE TRIGGER custgroup.TRG_CUST_ASSIGN_REL_ID
    BEFORE INSERT ON custgroup.T_CUSTOMER_ASSIGN_REL
    FOR EACH ROW
BEGIN
    IF :NEW.ID IS NULL THEN
        :NEW.ID := custgroup.SEQ_CUST_ASSIGN_REL.NEXTVAL;
    END IF;
END;
/


-- ------------------------------------------------------------
-- 4. 索引
-- ------------------------------------------------------------

-- 按营业部查所有客户关系（Manager Customers 列表关联查询）
CREATE INDEX IDX_CAR_BRANCH_NO
    ON custgroup.T_CUSTOMER_ASSIGN_REL (BRANCH_NO);

-- 按归属员工查名下客户（负载计算、员工绩效）
CREATE INDEX IDX_CAR_LOGIN_ID
    ON custgroup.T_CUSTOMER_ASSIGN_REL (LOGIN_ID, BRANCH_NO);

-- 按来源过滤（撤回接口校验 ASSIGN_SOURCE=1）
CREATE INDEX IDX_CAR_SOURCE
    ON custgroup.T_CUSTOMER_ASSIGN_REL (CLIENT_ID, ASSIGN_SOURCE);
