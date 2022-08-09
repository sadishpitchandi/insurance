import os,sys


class InsuranceException(Exception):

    def __init__(self, error_message:Exception,error_detail:sys) -> None:
        super().__init__(error_message)
        self.error_message=self.get_detailed_error_message(error_message=error_message,error_detail=error_detail)

    @staticmethod
    def get_detailed_error_message(error_message:Exception,error_detail:sys):
        
        _,_,exec_tb=error_detail.exc_info()

        file_name=exec_tb.tb_frame.f_code.co_filename
        tb_line_number=exec_tb.tb_lineno
        exception_block_line_number=exec_tb.tb_frame.f_lineno

        error_message=f"""Error occured in script:
        [ {file_name} ] 
        in try block line number: [{tb_line_number}] and exception block line number: [{exception_block_line_number}] 
        with error_message: [{error_message}]
        """

        return error_message

    def __str__(self) -> str:
        return self.error_message

    def __repr__(self) -> str:
        return InsuranceException.__name__.str()
