-- ============================================================
-- 客户分配记录表 DDL
-- 版本: V001
-- 说明: 记录每次客户分配操作，支持归属人/分配时间/分配人查询
-- ============================================================


-- ------------------------------------------------------------
-- 1. 主表
-- ------------------------------------------------------------
CREATE TABLE custgroup.T_CUSTOMER_ASSIGN_LOG
(
    ID           NUMBER          NOT NULL,            -- 主键，由序列生成
    CLIENT_ID    VARCHAR2(20)    NOT NULL,            -- 客户资金账号（关联 t_client_info.CLIENT_ID）
    BRANCH_NO    VARCHAR2(10)    NOT NULL,            -- 营业部编号（关联 Config.BRANCH_NO）
    LOGIN_ID     VARCHAR2(20)    NOT NULL,            -- 员工OA（被分配的理财经理）
    EMP_NAME     VARCHAR2(50),                        -- 员工姓名（冗余，避免频繁关联员工表）
    ASSIGN_TIME  TIMESTAMP       NOT NULL,            -- 本次分配发生时间
    LOGIN_ID_OP  VARCHAR2(20)    NOT NULL,            -- 分配人工号（执行分配操作的管理人员）
    EMP_NM_OP    VARCHAR2(50),                        -- 分配人姓名（冗余）
    REMARK       VARCHAR2(500),                       -- 分配备注（可选）
    CREATE_TIME  TIMESTAMP DEFAULT LOCALTIMESTAMP,      -- 记录落库时间
    CONSTRAINT PK_CUST_ASSIGN_LOG PRIMARY KEY (ID)
);

COMMENT ON TABLE  custgroup.T_CUSTOMER_ASSIGN_LOG                IS '客户分配记录表';
COMMENT ON COLUMN custgroup.T_CUSTOMER_ASSIGN_LOG.ID             IS '主键';
COMMENT ON COLUMN custgroup.T_CUSTOMER_ASSIGN_LOG.CLIENT_ID      IS '客户资金账号';
COMMENT ON COLUMN custgroup.T_CUSTOMER_ASSIGN_LOG.BRANCH_NO      IS '营业部编号';
COMMENT ON COLUMN custgroup.T_CUSTOMER_ASSIGN_LOG.LOGIN_ID       IS '员工OA，被分配的理财经理';
COMMENT ON COLUMN custgroup.T_CUSTOMER_ASSIGN_LOG.EMP_NAME       IS '员工姓名';
COMMENT ON COLUMN custgroup.T_CUSTOMER_ASSIGN_LOG.ASSIGN_TIME    IS '分配时间';
COMMENT ON COLUMN custgroup.T_CUSTOMER_ASSIGN_LOG.LOGIN_ID_OP    IS '分配人工号，执行分配操作的管理人员';
COMMENT ON COLUMN custgroup.T_CUSTOMER_ASSIGN_LOG.EMP_NM_OP      IS '分配人姓名';
COMMENT ON COLUMN custgroup.T_CUSTOMER_ASSIGN_LOG.REMARK         IS '分配备注';
COMMENT ON COLUMN custgroup.T_CUSTOMER_ASSIGN_LOG.CREATE_TIME    IS '记录创建时间';


-- ------------------------------------------------------------
-- 2. 主键序列
-- ------------------------------------------------------------
CREATE SEQUENCE custgroup.SEQ_CUST_ASSIGN_LOG
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;


-- ------------------------------------------------------------
-- 3. 触发器：INSERT 时自动填充 ID
-- ------------------------------------------------------------
CREATE OR REPLACE TRIGGER custgroup.TRG_CUST_ASSIGN_LOG_ID
    BEFORE INSERT ON custgroup.T_CUSTOMER_ASSIGN_LOG
    FOR EACH ROW                                         -- 行级触发器，:NEW 伪记录才可用
BEGIN
    IF :NEW.ID IS NULL THEN
        :NEW.ID := custgroup.SEQ_CUST_ASSIGN_LOG.NEXTVAL;
    END IF;
END;
/


-- ------------------------------------------------------------
-- 4. 索引
-- ------------------------------------------------------------

-- 核心查询：按客户取最新一条分配记录（PARTITION BY CLIENT_ID ORDER BY ASSIGN_TIME DESC）
CREATE INDEX IDX_CAL_CLIENT_ASSIGN
    ON custgroup.T_CUSTOMER_ASSIGN_LOG (CLIENT_ID, ASSIGN_TIME DESC);

-- 按营业部范围扫描（_fetch_assign_map 过滤 BRANCH_NO）
CREATE INDEX IDX_CAL_BRANCH_ASSIGN
    ON custgroup.T_CUSTOMER_ASSIGN_LOG (BRANCH_NO, ASSIGN_TIME DESC);

-- 按归属人查询名下所有客户（未来团队绩效分析页可能用到）
CREATE INDEX IDX_CAL_LOGIN_ID
    ON custgroup.T_CUSTOMER_ASSIGN_LOG (LOGIN_ID, ASSIGN_TIME DESC);
