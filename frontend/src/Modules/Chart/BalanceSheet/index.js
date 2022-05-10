import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { withStyles } from '@material-ui/core/styles';

import { styles } from './style';

import { creators as BalanceSheetActions } from '../../../Reducers/BalanceSheet';
import TopChart from "./TopChart";
import MiddleChart from "./MiddleChart";
import BottomChart from "./BottomChart";

class BalanceSheet extends Component {

  constructor(props) {
    super(props);

    this.state = {

    };

    this.handleFilter = this.handleFilter.bind(this);
  }

  componentDidMount() {
    console.log('Balance Sheet');
    const { defaultDimDate } = this.props;
    this.props.updateFilter({dimDate:defaultDimDate});
    this.props.getBalanceSheetQuerys(defaultDimDate);
   }

  componentWillUnmount() {

  }

  handleFilter = (event) => {

    this.props.updateFilter(event);
    
  };

  render() {
    const { classes, dir,queryResult, dimDate} = this.props;

    return (
      <div className={classes.root} dir={dir}>

          <TopChart 
              queryData={queryResult}
              dimDate={dimDate}
              handleFilter={this.handleFilter}
            />
            <MiddleChart 
              queryData={queryResult}
              dimDate={dimDate}
              handleFilter={this.handleFilter}
            />
            <BottomChart 
              queryData={queryResult}
              dimDate={dimDate}
              handleFilter={this.handleFilter}
            />

        
      </div>
    );
  }

}


BalanceSheet.propTypes = {
  classes: PropTypes.object.isRequired,
  dir: PropTypes.string.isRequired,
  dimDate: PropTypes.string.isRequired,
  queryResult: PropTypes.object.isRequired,
  defaultYear: PropTypes.number.isRequired,
  defaultMonth: PropTypes.number.isRequired,
  defaultDimDate: PropTypes.string.isRequired,
};

const mapStateToProps = state => {
  return {
    queryResult: state.BalanceSheet.queryResult,
    dimDate: state.BalanceSheet.dimDate,
  }
}; 

const mapDispatchToProps = (dispatch) => {
  return {
    updateFilter: (filter) => dispatch(BalanceSheetActions.glbsUpdateFilter(filter)),
    getBalanceSheetQuerys: (dimDate) => dispatch(BalanceSheetActions.glbsQuerysRequest(dimDate)),
  }
};

export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(BalanceSheet));
