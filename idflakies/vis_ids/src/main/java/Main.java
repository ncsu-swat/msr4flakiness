import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.PackageDeclaration;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.VariableDeclarator;
import com.github.javaparser.ast.body.Parameter;
import com.github.javaparser.ast.expr.FieldAccessExpr;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.expr.NameExpr;
import com.github.javaparser.ast.expr.StringLiteralExpr;
import com.github.javaparser.ast.stmt.BlockStmt;
import com.github.javaparser.ast.comments.LineComment;
import com.github.javaparser.ast.comments.BlockComment;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.ByteArrayInputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.HashSet;
import java.nio.charset.StandardCharsets;

public class Main {

    public static void listNames(String fileName) throws Exception {
        HashSet<String> ids = new HashSet<String>();
        class IdentifierVisitor extends VoidVisitorAdapter<Void> {
            @Override
            public void visit(VariableDeclarator vd, Void ignore) {
                super.visit(vd, ignore);
                ids.add(vd.getName().getIdentifier());
            }
            @Override
            public void visit(NameExpr ne, Void ignore) {
                super.visit(ne, ignore);
                ids.add(ne.getName().getIdentifier());
            }
            @Override
            public void visit(MethodDeclaration md, Void ignore) {
                super.visit(md, ignore);
                ids.add(md.getNameAsString());
            }

            @Override
            public void visit(MethodCallExpr mc, Void ignore) {
                super.visit(mc, ignore);
                ids.add(mc.getName().getIdentifier());
            }

            @Override
            public void visit(StringLiteralExpr sl, Void ignore) {
                super.visit(sl, ignore);
                ids.add(sl.asString());
            }

            @Override
            public void visit(BlockComment bc, Void ignore) {
                super.visit(bc, ignore);
                ids.add(bc.getContent());
            }                                                

            @Override
            public void visit(LineComment lc, Void ignore) {
                super.visit(lc, ignore);
                ids.add(lc.getContent());
            }                                                
        }
        
        // mock complete class to enable parsing from method (test case)
        File temp = File.createTempFile("tempfile", ".tmp"); 
        BufferedWriter bw = new BufferedWriter(new FileWriter(temp));
        StringBuffer sb = new StringBuffer();
        sb.append("public class Main {");
        sb.append(System.lineSeparator());        
        try (BufferedReader br = new BufferedReader(new FileReader(fileName))) { //StandardCharsets.UTF_8
            String line;
            while ((line = br.readLine()) != null) {
                sb.append(line);
                sb.append(System.lineSeparator());
            }
        }
        sb.append("}");
        bw.write(sb.toString());
        bw.close();

        // reporting identifiers
        FileInputStream in = new FileInputStream(temp.getAbsolutePath());
        CompilationUnit compUnit;
        try {
            compUnit = StaticJavaParser.parse(in);
            compUnit.accept(new IdentifierVisitor(), null);
            List<String> stopWords = java.util.Arrays.asList(new String[]{"println","java","japa","org","Override","Exception","x","i","s","hello"});
            for (String s : ids) {
                if (!stopWords.contains(s)) System.out.println(s);
            }
        } finally {
            in.close();
        }
    }

    public static void main(String[] args) throws Exception {
        String x = "hello";
        Main.listNames(args[0]);
    }
}
