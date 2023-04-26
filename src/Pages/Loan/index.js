import React, { useEffect, useState } from 'react';
import { Layout, Table, Row, Col, message } from 'antd';
import LoansAPI from '../../API/Services/Loan';
import Header from '../../Layouts/Header';
import { Link } from 'react-router-dom';

const { Content, Footer } = Layout;
const contentStyle = {
    textAlign: 'center',
    padding: '0 50px',
    margin: '16px 0 0 0'
};

const Loan = (props) => {
    const [loans, setLoans] = useState([]);
    const [getLoanDone, setGetLoanDone] = useState(false);
    const [triggerGetLoan] = useState(false);

    useEffect(() => {
        LoansAPI.GetLoans()
            .then((response) => {
                const loans = response.data.loans;
                setLoans(loans.map((project) => ({
                    key: project.PROJECT_ID,
                    id: project.PROJECT_ID,
                    managerID: project.MANAGER_ID,
                    name: project.P_NAME,
                    startDate: project.START_DATE,
                    expectedEndDate: project.EXPECTED_END_DATE,
                    actualEndDate: project.ACTUAL_END_DATE,
                    description: project.P_DESCRIPTION,
                    budget: project.BUDGET
                })))
                setGetLoanDone(true);
            }).catch(err => {
                message.error(err.response.data.error);
            })
    }, [triggerGetLoan])
    
    const loadingProps = {
        spinning: !getLoanDone
    }

    const loanColumns = [
        { title: 'ID', dataIndex: 'id', key: 'id' },
        {},
        { 
            title: 'Name', dataIndex: 'name', key: 'name',
            render: (_, record) => <Link to={`/loans/${record.id}/personnels`}> {record.name} </Link> 
        },
        { title: 'Manager ID', dataIndex: 'managerID', key: 'managerID' },
        { 
            title: 'Start Date', dataIndex: 'startDate', key: 'startDate',
            render: (date) => date ? new Date(date).toLocaleDateString('vi-VN') : date
        },
        { 
            title: 'Expected End Date', dataIndex: 'expectedEndDate', key: 'expectedEndDate',
            render: (date) => date ? new Date(date).toLocaleDateString('vi-VN') : date
        },
        { 
            title: 'Actual End Date', dataIndex: 'actualEndDate', key: 'actualEndDate',            
            render: (date) => date ? new Date(date).toLocaleDateString('vi-VN') : date
        },
        { title: 'Description', dataIndex: 'description', key: 'description' },
        { 
            title: 'Budget', dataIndex: 'budget', key: 'budget',
            render: (budget) => budget ? budget.toLocaleString('vi-VN') : budget
         },
    ]

    return <Layout>
        <Header selectedKey={'1'}/>
        <Content style={contentStyle}>
            <Row gutter={[0, 0]} align="middle">
                <Col span={24}>
                    <h1 className='custom-h1-header'>
                        Loans
                    </h1>
                </Col>
            </Row>
            <div className='site-layout-content'>
                <div className='site-content'>
                    <Table columns={loanColumns} dataSource={loans} loading={loadingProps} />
                </div>
            </div>
        </Content>
        <Footer />
    </Layout>
}

export default Loan;